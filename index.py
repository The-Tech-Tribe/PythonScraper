from flask import Flask, request, jsonify
from pprint import pprint

from crunchbase import get_company_id, get_fields

app = Flask(__name__)


# 127.0.0.1:5000/socials?name=google
@app.route("/socials/", methods=["GET"])
def get_socials():
    args = request.args
    name = args.get('name')

    entity_id = get_company_id(name)
    fields = get_fields(entity_id)

    twitter_uri = ''
    linkedin_uri = ''
    facebook_uri = ''
    short_description = ''

    pprint(fields)
    if "twitter" in fields:
        twitter_uri = fields.get("twitter").get("value")
    if "linkedin" in fields:
        linkedin_uri = fields.get("linkedin").get("value")
    if "facebook" in fields:
        facebook_uri = fields.get("facebook").get("value")
    if "short_description" in fields:
        short_description = fields.get("short_description")

    response = {
        "twitter": twitter_uri,
        "linkedin": linkedin_uri,
        "facebook": facebook_uri,
        "short_description": short_description
    }

    return jsonify(response)


app.run()
