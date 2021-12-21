import requests
from bs4 import BeautifulSoup
from random import randint
import re 

url = 'https://nytimes.com'

def get_poem(url, lines, words): # scrapes headlines, adds words to a list, selects them at random and formats them as a poem. 

    words_per_line = randint(1, words)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    headlines = [headline.text for headline in soup.find_all('h3')]

    word_pool = []
    conjunctions = []

    statement = ""
    poem = []
    
    #collect words and put them into lists (word_pool and conjunctions)
    for i in range(len(headlines)):
        abbrev = headlines[i].split()
        for word in abbrev:
            word = re.sub(r'[.?,:".>]', '', word)
            if word in ('and', 'but', 'if', 'because', 'or'): #conjuctions
                conjunctions.append(word.lower())
            else:
                word_pool.append(word.lower())

    for i in range(lines):
    #make a line of words
        statement = ""
        for i in range(words_per_line): #length of each line
            # if you want to add conjunctions
            if i == 4: 
                statement += f'{conjunctions[randint(0, len(conjunctions)-1)]} '
            else:
                word_selector = randint(0, len(word_pool)-1)
                statement += f'{word_pool[word_selector]} '
                words_per_line = randint(1, words)
        poem.append(statement)


    # print(type(statement))
    return poem
    

# if __name__ == "__main__":
#     print(get_poem(url, 5, 10))


