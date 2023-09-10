# https://idno.md/companii?q=1003600042004

import requests
from bs4 import BeautifulSoup
import json


class CompanyIdnoScraper:
    def __init__(self, company_idno):
        self.company_idno = company_idno
        self.search_url = f'https://idno.md/companii?q={self.company_idno}'
        self.company_url = ''
        self.company_info = {}
        self.company_history = {}

    def get_company_url(self):
        page = requests.get(self.search_url)
        soup = BeautifulSoup(page.content, "html.parser")
        rows = soup.select('#companies tr')
        second_row = rows[1]
        link = second_row.select_one('a')['href']
        self.company_url = f'https://idno.md/{link}'

    def get_company_info(self):
        self.get_company_url()
        page = requests.get(self.company_url)
        soup = BeautifulSoup(page.content, "html.parser")
        data = {}
        history_details = {}

        sections = soup.select('.row > .col-md-6')

        for section in sections:
            title_elem = section.select_one('.ftitle')
            content_elem = section.select_one('p')

            if title_elem and content_elem:
                title_text = title_elem.get_text().strip()
                content_text = content_elem.get_text().strip()

                if "a" in content_elem.decode_contents():
                    content_text = [a.get_text().strip() for a in content_elem.select('a')]

                data[title_text] = content_text

        history_container = soup.find('div', {'class': 'container history'})

        if history_container:
            history_section = history_container.find('div', {'class': 'col-md-10 col-xs-10'})

            if history_section:
                for p_tag in history_section.find_all('p')[1:]:
                    text_content = p_tag.get_text().strip()
                    try:
                        date, info = text_content.split(' ', 1)
                        history_details[date] = info
                    except ValueError:
                        print(f"Skipping: {text_content}")

        self.company_info = json.dumps(data)
        self.company_history = json.dumps(history_details, indent=4)


if __name__ == "__main__":
    si = CompanyIdnoScraper(1003600042004)
    si.get_company_info()
    print(si.company_info)
    print(si.company_history)
