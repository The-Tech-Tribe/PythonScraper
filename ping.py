import requests
url = 'http://127.0.0.1:5000/ss'

data = {
    "company": "linella"
}

data_post = requests.post(url, json=data)
print(data_post.text)