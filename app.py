from flask import Flask, jsonify, request
from UnifiedScraper import UnifiedCompanyScraper
import openai

openai.api_key = "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"
app = Flask(__name__)


@app.route('/ss', methods=['POST'])
def scraper():
    crunchbase_user_key = '6827e0f7db8526fcc95f200cac677aa0'
    openai_api_key = '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'
    data = request.get_json()
    token = data["company"]

    sc = UnifiedCompanyScraper(token, openai_api_key, crunchbase_user_key)
    sc.fetch_all()

    result = sc.merge_and_gptfy2x()

    return jsonify({
        "description": result
    })


app.run()
