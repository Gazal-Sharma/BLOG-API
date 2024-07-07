from flask import Flask, render_template
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from blog.blueprints.blogpost.blogpost import blog_post
from blog.blueprints.comments.comments import comments
from blog.blueprints.user_details.user import user
app = Flask(__name__)

# configuring database
DB_CONFIG = {
    'dbname' : "blogapi",
    'user': "edc",
    'password': 'icandothis12357',
    'host': "localhost",
    'port': "5432"
}

# setting up database connection
def db_connection():
    conn = psycopg2.connect(
        dbname = DB_CONFIG['dbname'],
        user = DB_CONFIG['user'],
        password = DB_CONFIG['password'],
        host = DB_CONFIG['host'],
        port = DB_CONFIG['port']
    )
    return conn

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://edc:icandothis12357@localhost/blogapi'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'your_secret_key'
# function to create tables for storing content
def create_tables():
    conn = db_connection()
    if conn is None:
        return 
    cur = conn.cursor()
    with open('sql_table.sql','r') as f:
        cur.execute(f.read())
    conn.commit()
    cur.close()
    conn.close()

## login and user authentication
    
##other blueprint register
app.register_blueprint(blog_post, url_prefix = '/blogpt')
app.register_blueprint(comments, url_prefix = '/comment')
app.register_blueprint(user, url_prefix = '/users')
# running app with debug

@app.route('/')
def home():
    return render_template('base.html')
    
if __name__ == "__main__":
    create_tables()
    app.run(debug = True)