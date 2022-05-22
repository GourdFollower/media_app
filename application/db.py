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


def close_db():
    db = g.pop('db', None)

    if db is not None:
        db.close()


"""def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    ""Clear the existing data and create new tables.""
    init_db()
    click.echo('Initialized the database.')"""


def version():
    db = get_db()
    with db.cursor() as cur:
        cur.execute('SELECT VERSION()')
        version = cur.fetchone()
        print(f'Database version: {version[0]}')
