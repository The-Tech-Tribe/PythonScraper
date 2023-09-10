import requests
from pprint import pprint
import urllib.parse


# sample: entity_id = '6acfa7da-1dbd-936e-d985-cf07a1b27711' - google


def get_company_id(name):
    url = "https://api.crunchbase.com/api/v4/autocompletes"
    headers = {
        "Content-Type": "application/json",
    }

    params = {
        "user_key": "6827e0f7db8526fcc95f200cac677aa0",
        "query": name,
        "limit": 1
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()['entities'][0]['identifier']['uuid']


def get_fields(entity_id):
    url = f"https://api.crunchbase.com/api/v4/entities/organizations/{entity_id}?"
    headers = {
        "Content-Type": "application/json",
    }

    params = {
        "user_key": "6827e0f7db8526fcc95f200cac677aa0",
        "card_ids": ['fields', 'founders']
    }

    response = requests.get(url, headers=headers, params=params)

    return response.json()['cards']['fields']
