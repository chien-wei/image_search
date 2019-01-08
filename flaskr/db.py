import click
from flask import current_app, g
from flask.cli import with_appcontext
from pymongo import MongoClient
import pickle
from multiprobe_lsh import MultiprobeLSH



def get_mongo_client():
    if 'mp' not in g:
        with open('tables.pickle2', 'rb') as file:
            g.mp = pickle.load(file)
    return g.mp


def close_mongo_client(e=None):
    pass


def init_client():
    mp = get_mongo_client()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_client()

def init_app(app):
    app.teardown_appcontext(close_mongo_client)
    app.cli.add_command(init_db_command)

