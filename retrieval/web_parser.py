import trafilatura
import requests

def fetch_article(url):
    response = requests.get(url, timeout=10)
    return trafilatura.extract(response.text)