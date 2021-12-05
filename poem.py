import requests
from bs4 import BeautifulSoup
from random import randint
import re 

url = 'https://finance.yahoo.com/quote/AAPL/history?p=AAPL'
url2 = 'https://nytimes.com'


def get_poem(url, lines, words):

    words_per_line = randint(1, words)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    headlines = [headline.text for headline in soup.find_all('h3')]

    #word_pool len is 642 (number of words aggreted)
    word_pool = []
    conjunctions = []

    statement = ""

    #collect words and put them into lists (word_pool and conjunctions)
    for i in range(len(headlines)):
        abbrev = headlines[i].split()
        for word in abbrev:
            word = re.sub(r'[.?,:".>]', '', word)
            if word in ('and', 'but', 'if', 'because'): #conjuctions
                conjunctions.append(word.lower())
            else:
                word_pool.append(word.lower())

    for i in range(lines):
    #make a line words
        for i in range(words_per_line): #length of each line
            if i == 2 or i == 5:
                statement += f'{conjunctions[randint(0, len(conjunctions)-1)]} '
            else:
                word_selector = randint(0, len(word_pool)-1)
                statement += f'{word_pool[word_selector]} '
            words_per_line = randint(1, words)
        statement += '\n'
    print(statement)
    

if __name__ == "__main__":
    get_poem(url2, 7, 10)


