from flask import Flask, session, redirect, url_for, request, render_template, current_app, g, flash
import requests
from bs4 import BeautifulSoup
from random import randint

###TEST

# gets a random image from the times homepage and displays it on an index html page
app = Flask(__name__)

url = 'https://nytimes.com'

def get_pic():
    print('....... getting images .......')
    images = []

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    imgs = soup.findAll('img')

    for img in imgs:
        image_url = img['src']
        images.append(image_url)

    random_index = randint(1, len(images)-1)
    return images[random_index] # change number to get a diff one from list



@app.route('/')
def show_pic():
    pic = get_pic()
    return render_template('index.html', pic=pic)


if __name__ == '__main__':
    app.run(debug=True)