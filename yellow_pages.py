import requests
from bs4 import BeautifulSoup
import json
import openai


class CompanyScraperYellowPages:
    def __init__(self, search, openai_api_key):
        self.search = search
        self.search_url = f"https://www.yellowpages.md/companies/list/?search={search}"
        self.company_idno = ""
        openai.api_key = openai_api_key

    def get_company_url(self):
        page = requests.get(self.search_url)
        soup = BeautifulSoup(page.content, "html.parser")
        a_tag = soup.find('a', {'class': 'yp_company_url'})
        company_url = a_tag['href'] if a_tag else None
        return company_url

    def get_company_info(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        company_info = {}

        for company_div in soup.find_all('div', {'class': 'company_info'}):
            left_div = company_div.find('div', {'class': 'column_info column_left'})
            right_div = company_div.find('div', {'class': 'column_info column_right'})

            left_text = left_div.get_text().strip() if left_div else None
            right_text = right_div.get_text().strip() if right_div else None

            if left_text and right_text:
                company_info[left_text] = right_text

        company_info_json = json.dumps(company_info, ensure_ascii=False)
        self.company_idno = company_info.get("IDNO:", None)
        return company_info_json

    def gptfy(self):
        company_url = self.get_company_url()
        company_info = self.get_company_info(company_url)

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": f"having this text create a short summary about the company {company_info}"
            }]
        )

        return completion.choices[0].message.content, self.company_idno


if __name__ == "__main__":
    search = 'linella'
    api_key = "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"
    scraper = CompanyScraperYellowPages(search, api_key)
    summary = scraper.gptfy()
