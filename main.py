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
    error = None

    if request.method=='POST':
        if request.form['username'] != check_username:
            error = 'Incorrect username'
        elif request.form['password'] != check_password:
            error = 'Incorrect password'
        else:
        #     session['logged_in'] = True 
            return redirect(url_for('dashboard'))

    return render_template('login.html', error=error)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', copy=[1,2,3,4,5])


if __name__ == '__main__':
    app.run(debug=True)