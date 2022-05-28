import click
from flask import current_app, g
from flask.cli import with_appcontext

import pymysql


# gives outside app context error
"""current_app.config['MYSQL_HOST'] = 'localhost'
current_app.config['MYSQL_USER'] = 'root'
current_app.config['MYSQL_PASSWORD'] = 'B4lr0gsAbound'
current_app.config['MYSQL_DB'] = 'media_app'"""


def connection():
    s = 'localhost'
    d = 'media_app'
    u = 'root'
    p = 'B4lr0gsAbound'
    conn = pymysql.connect(host=s, user=u, password=p, database=d)
    return conn


def get_db():
    if 'db' not in g:
        g.db = connection()

    return g.db


def close_db(): # in flask documentation, takes argument e=None. Idk what that means
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with db.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS user, media;")
        user = """CREATE TABLE user ( id INT NOT NULL AUTO_INCREMENT,
               username VARCHAR(255) UNIQUE NOT NULL, password VARCHAR(255) NOT NULL, PRIMARY KEY (id) );"""
        cur.execute(user)

        media = """CREATE TABLE media ( id INT NOT NULL AUTO_INCREMENT, author_id INT NOT NULL,
        title VARCHAR(255) NOT NULL, type VARCHAR(255), ranking INT, PRIMARY KEY (id), 
        FOREIGN KEY (author_id) REFERENCES user(id));"""
        cur.execute(media)
        cur.close()


# these two functions are currently not working
# the first cannot locate a Flask application -- FLASK_APP environment variable needs to set?
# and it says "wsgi.py" or "app.py" module not found in current directory

@click.command('init-db')
@with_appcontext
def init_db_command():
    """"Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
