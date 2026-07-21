import requests
from datetime import date, timedelta
import os
from dotenv import load_dotenv


def fetch_articles():
    load_dotenv()
    YESTERDAY = date.today() - timedelta(days = 1)
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    
    url = 'https://newsapi.org/v2/everything?'
    params = {
        'q': 'AI OR "Computer Science" OR "Machine Learning"',
        'from': YESTERDAY,                
        'sortBy': 'publishedAt',                
        'apiKey': NEWS_API_KEY,        
        'language': 'en',
        'excludeDomains': 'pypi.org' # don't want python packages
        }

    r = requests.get(url, params= params)
    
    if r.ok:
        return r.json()
    raise RuntimeError("Unable to fetch articles")

print(fetch_articles())