import openai
import json
from crunchbase import get_company_id, get_fields
from yellow_pages import CompanyScraperYellowPages
from idno import CompanyIdnoScraper


class UnifiedCompanyScraper:
    def __init__(self, company_name, openai_api_key, crunchbase_user_key):
        self.company_name = company_name
        self.openai_api_key = openai_api_key
        self.crunchbase_user_key = crunchbase_user_key
        self.company_info = {}
        self.company_idno = None
        self.company_info_based_idno = {}
        self.company_history_based_idno = {}
        self.company_summary_info_gpt = {}

    def scrape_from_yellowpages(self):
        scraper_yp = CompanyScraperYellowPages(self.company_name, self.openai_api_key)

        self.company_info['yellowpages'], self.company_idno = scraper_yp.gptfy()

    def scrape_from_crunchbase(self):
        entity_id = get_company_id(self.company_name)

        self.company_info['crunchbase'] = get_fields(entity_id)

    def scrape_from_idno(self):
        scraper_id = CompanyIdnoScraper(self.company_idno)
        scraper_id.get_company_info()

        self.company_info_based_idno = scraper_id.company_info
        self.company_history_based_idno = scraper_id.company_history

    def summarize_with_openai(self):
        openai.api_key = self.openai_api_key

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": f"Please summarize the company information: {self.company_info}"
            }]
        )
        self.company_info['summary'] = completion.choices[0].message.content
        self.company_summary_info_gpt = self.company_info['summary']

    def fetch_all(self):
        self.scrape_from_yellowpages()
        self.scrape_from_crunchbase()
        self.summarize_with_openai()
        if self.company_idno is not None:
            self.scrape_from_idno()

    def prinf_all_company_info(self):
        self.fetch_all()

        print(self.company_summary_info_gpt)
        print(self.company_info)
        print(self.company_info_based_idno)
        print(self.company_history_based_idno)
        print(self.company_idno)

    def merge_and_gptfy2x(self):
        merged_info = str(self.company_info) + '' + str(self.company_info_based_idno) + '' + str(self.company_history_based_idno)

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": f"having this text create a summary about the company"
                           f"based on {merged_info} "
                           f"and add their website and social media links if there are"
            }]
        )

        return completion.choices[0].message.content


if __name__ == '__main__':
    company_name = 'amdaris'
    openai_api_key = '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'
    crunchbase_user_key = '6827e0f7db8526fcc95f200cac677aa0'

    scraper = UnifiedCompanyScraper(company_name, openai_api_key, crunchbase_user_key)
    scraper.prinf_all_company_info()
    print(scraper.merge_and_gptfy2x())





