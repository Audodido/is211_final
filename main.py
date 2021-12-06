from flask import Flask, session, redirect, url_for, request, render_template, current_app, g, flash
import requests
from bs4 import BeautifulSoup
from random import randint
import poem


app = Flask(__name__)

check_username = 'admin'
check_password = 'password'


@app.route('/')
def main_page():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    pass


if __name__ == '__main__':
    app.run(debug=True)