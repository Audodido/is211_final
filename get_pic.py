import requests
from bs4 import BeautifulSoup
from random import randint
import re 
import wget # make sure to leave a note for professor that wget package must be installed


url = 'https://nytimes.com'


def get_pic():
    print('....... getting images .......')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    imgs = soup.findAll('img')
    my_path = '/Users/connorhanwick/Desktop/Python/is_211/final'

    i = 0

    for img in imgs:
        image_url = img['src']
        destination = f'{my_path}/img{i}'
        print(image_url)
        print(destination)
        wget.download(image_url, destination)
        i += 1


if __name__ == '__main__':
    get_pic()


