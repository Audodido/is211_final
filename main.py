from flask import Flask, session, redirect, url_for, request, render_template   
import sqlite3
from poem import get_poem
from datetime import datetime
from headlines import getAllHeadlines
from os.path import exists

app = Flask(__name__)


url = 'https://nytimes.com'
check_username = 'admin'
check_password = 'password'
app.secret_key = '\xbb\xcc\xdbS-\xcb\x99\xc3\xf5\xe7&\x87\xcc\xef\x98\x86\x80[\xcd\xad\x05\xf6\xfd\xd2'


today = datetime.today().strftime('%Y-%m-%d')
login_error = "Sorry — you must log in to access that feature."


conn = sqlite3.connect('blog_posts.db') #connect to the database in same thread/method !!change to g.db!!
cur = conn.cursor() 
cur.execute('DROP TABLE IF EXISTS posts')
# create + populate table with existing posts
cur.execute('''CREATE TABLE IF NOT EXISTS posts ( 
            date DATE,
            user INTEGER,
            entry_title TEXT
            )''')


def get_posts(): #returns any posts in the database
    conn = sqlite3.connect('blog_posts.db') 
    cur = conn.cursor() 

    cur.execute('SELECT rowid, date, user, entry_title FROM posts ORDER BY rowid DESC') # retreived in descending order by date. So the need not necessarily stored as a stack but retreived as if they were
    post_results = cur.fetchall()
    return post_results


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

    conn = sqlite3.connect('blog_posts.db')
    cur = conn.cursor()
    cur.execute("SELECT entry_title FROM posts") 
    posts = cur.fetchall()
    return render_template('login.html', error=error, posts=posts)



def write_file(title, str): #writes blogpost to a .txt file and stores associated post data in the database
    conn = sqlite3.connect('blog_posts.db') 
    cur = conn.cursor() 

    with open(f'{title}.txt', 'w+') as f:
        f.write(str)
    
    cur.execute('INSERT INTO posts VALUES (?,?,?)', (today, 1, title))
    conn.commit()


# takes a blog entry title and returns corresponding rowid 
def get_id(title):
    conn = sqlite3.connect('blog_posts.db') #connect to the database in same thread/method !!change to g.db!!
    cur = conn.cursor() 

    cur.execute('SELECT rowid FROM posts WHERE entry_title == ?;', [title])
    id = cur.fetchone()
    print(id)
    return id


@app.route('/dashboard')
def dashboard():

    if not session.get('logged_in'): # check if user is logged in
            return redirect('/login')       
    else:
        return render_template('dashboard.html', copy=get_posts()) 


@app.route('/createpost', methods=['GET', 'POST'])
def create_post():
    if not session.get('logged_in'):
            return redirect('/login')
    else:
        if request.method == 'GET':
            headlines = getAllHeadlines(url) # calls function from headlines.py module to get scraped headlines to choose from 
            return render_template('create_post.html', headlines=headlines)
        
        elif request.method == 'POST':
            title = request.form['foo'] 
            copy = " ".join(get_poem(url, 5, 10)) #create a poem
            
            write_file(title, copy) #write the file and add its metadata to the database
            id = get_id(title) #get rowid for the new blog entry

        return redirect(url_for('post', id=id))


@app.route('/post/edit/<id>', methods=['POST'])
def edit_post(id):
    if not session.get('logged_in'):
            return redirect('/login')
    else:
        conn = sqlite3.connect('blog_posts.db') 
        cur = conn.cursor() 

        edited_title = request.form['blogtitle'].strip()
        edited_poem = request.form['blogcopy'].strip()

        cur.execute('UPDATE posts SET entry_title = ? WHERE rowid = ?', (edited_title, id))

        with open(f'{edited_title}.txt', 'w+') as f:
            f.write(edited_poem)
        
        conn.commit()

        return redirect('/dashboard')


@app.route('/deletepost/<id>', methods=['POST'])
def delete_post(id):
    if not session.get('logged_in'):
            return redirect('/login')
            
    else:
        if request.method=='POST':
            conn = sqlite3.connect('blog_posts.db') 
            cur = conn.cursor()         

            cur.execute('DELETE FROM posts WHERE rowid == ?', (id,))

            conn.commit()
            
            return redirect('/dashboard')


@app.route('/post/<id>', methods=['GET', 'POST'])
def post(id):
    if not session.get('logged_in'):
            return redirect('/login')

    else:
        edit = False
        if request.method=='GET': 
            conn = sqlite3.connect('blog_posts.db') 
            cur = conn.cursor() 

            cur.execute('SELECT * FROM posts WHERE rowid == ?', (id,))
            results = cur.fetchone()
            title = results[2] 

            with open(f'{title}.txt', 'r+') as f:
                post = f.read()

            return render_template('post.html', edit=edit, title=title, post=post, id=id) 

        elif request.method=='POST':

            edit = True
            conn = sqlite3.connect('blog_posts.db') 
            cur = conn.cursor() 

            cur.execute('SELECT * FROM posts WHERE rowid == ?', id)
            results = cur.fetchone()
            title = results[2]
            
            with open(f'{title}.txt', 'r+') as f:
                post = f.read()

            return render_template('post.html', edit=edit, title=title, post=post, id=id) 


if __name__ == '__main__':
    app.run(debug=True)