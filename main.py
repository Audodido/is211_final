from flask import Flask, session, redirect, url_for, request, render_template, current_app, g, flash
import sqlite3
import requests
from bs4 import BeautifulSoup
from random import randint
from poem import get_poem
from datetime import datetime
import os
import re 
from headlines import getAllHeadlines



app = Flask(__name__)

url = 'https://nytimes.com'
check_username = 'admin'
check_password = 'password'
app.secret_key = '\xbb\xcc\xdbS-\xcb\x99\xc3\xf5\xe7&\x87\xcc\xef\x98\x86\x80[\xcd\xad\x05\xf6\xfd\xd2'


## don't need this dict, right???
posts = {
    '2021-12-06' : (1, 'post1'),
    '2021-12-05' : (1, 'post2')
}

today = datetime.today().strftime('%Y-%m-%d')


### SQL STUFF START SQL STUFF START SQL STUFF START SQL STUFF START SQL STUFF START SQL STUFF START 

conn = sqlite3.connect('blog_posts.db') #connect to the database in same thread/method !!change to g.db!!
cur = conn.cursor() 


cur.execute('DROP TABLE IF EXISTS posts')
#create + populate table with existing posts
cur.execute('''CREATE TABLE IF NOT EXISTS posts ( 
            date DATE,
            user INTEGER,
            entry_title TEXT
            )''')

def populate_table(dict):
    for k, v in dict.items():
        cur.execute('INSERT INTO posts VALUES (?,?,?)', (k,v[0], v[1]))

    conn.commit()

populate_table(posts)

def get_posts():
    conn = sqlite3.connect('blog_posts.db') #connect to the database in same thread/method !!change to g.db!!
    cur = conn.cursor() 

    cur.execute('SELECT rowid, date, user, entry_title FROM posts ORDER BY rowid DESC') # retreived in descending order by date. So the need not necessarily stored as a stack but retreived as if they were
    post_results = cur.fetchall()
    return post_results


### SQL STUFF END SQL STUFF END SQL STUFF END SQL STUFF END SQL STUFF END SQL STUFF END SQL STUFF END 


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
            session['logged_in'] = True 
            return redirect(url_for('dashboard'))

    conn = sqlite3.connect('blog_posts.db') #connect to the database in same thread/method !!change to g.db!!
    cur = conn.cursor()
    cur.execute("SELECT entry_title FROM posts") 
    posts = cur.fetchall()
    return render_template('login.html', error=error, posts=posts)


# create/store a txt file with copy from crewate_post,.html with blog title as filename
# then add post to sql db
def write_file(title, str):
    conn = sqlite3.connect('blog_posts.db') #connect to the database in same thread/method !!change to g.db!!
    cur = conn.cursor() 


    with open(f'{title}.txt', 'w+') as f:
        f.write(str)
    
    cur.execute('INSERT INTO posts VALUES (?,?,?)', (today, 1, title))
    conn.commit()

# gets rowid from db where entry_title equals title parameter
def get_id(title):
    conn = sqlite3.connect('blog_posts.db') #connect to the database in same thread/method !!change to g.db!!
    cur = conn.cursor() 

    cur.execute('SELECT rowid FROM posts WHERE entry_title == ?;', [title])
    id = cur.fetchone()
    print(id)
    return id

@app.route('/dashboard')
def dashboard():
    if session['logged_in'] == True:
        return render_template('dashboard.html', copy=get_posts()) 
        

@app.route('/createpost', methods=['GET', 'POST'])
def create_post():
    if request.method == 'GET':
        #call function from headlines module to get headlines to choose from 
        headlines = getAllHeadlines(url)
        return render_template('create_post.html', headlines=headlines)
    elif request.method == 'POST':
        title = request.form['foo'] #radio button answer 

        copy = " ".join(get_poem(url, 5, 10)) #create a poem
        # print(title)
        # print(copy)
        
        write_file(title, copy) #write the file to the database
        
        id = get_id(title) #call up the id for the new blog entry

    return redirect(url_for('post', id=id))


@app.route('/deletepost', methods=['POST'])
def delete_post():
    post_to_delete = request.form['action'].replace('delete', '')
    post_to_delete = int(post_to_delete.strip())

    conn = sqlite3.connect('blog_posts.db') #connect to the database in same thread/method !!change to g.db!!
    cur = conn.cursor() 

    cur.execute("DELETE FROM posts WHERE rowid == ?;" (post_to_delete))

    conn.commit()

    return render_template('/dashboard')



@app.route('/post/<id>', methods=['GET', 'POST'])
def post(id):
    edit = False
    if request.method=='GET': #need this or no?
        conn = sqlite3.connect('blog_posts.db') #connect to the database in same thread/method !!change to g.db!!
        cur = conn.cursor() 

        cur.execute('SELECT * FROM posts WHERE rowid == ?', (id,))
        results = cur.fetchone()
        title = results[2]

        with open(f'{title}.txt', 'r+') as f:
            post = f.read()

        return render_template('post.html', edit=edit, title=title, post=post) #change to actual post


    elif request.method=='POST': #need this or no?

        edit = True
        conn = sqlite3.connect('blog_posts.db') #connect to the database in same thread/method !!change to g.db!!
        cur = conn.cursor() 

        cur.execute('SELECT * FROM posts WHERE rowid == ?', id)
        results = cur.fetchone()
        title = results[2]
        

        with open(f'{title}.txt', 'r+') as f:
            post = f.read()

        return render_template('post.html', edit=edit, title=title, post=post) #change to actual post


if __name__ == '__main__':
    app.run(debug=True)