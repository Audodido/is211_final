import requests
from bs4 import BeautifulSoup
from random import randint
import re 
import pprint

url = 'https://nytimes.com'

def getAllHeadlines(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    headlines = [headline.text for headline in soup.find_all('h3')]

    # for line in headlines:
    return headlines


# pprint.pprint(getAllHeadlines(url))