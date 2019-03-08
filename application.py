#! /usr/bin/python3
#! -*- coding: utf-8 -*-


import json
import os
import platform
from flask import Flask, render_template, make_response, request
from flask_session import Session

# Enable ORM.
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


# Initialize and configure the application.
app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'

# Initialize session.
Session(app)

# Set up database and database engine.
os.environ['DATABASE_URL'] = 'postgres://wg_forge:a42@localhost:5432/wg_forge_db'
engine = create_engine(os.getenv('DATABASE_URL'))
db = scoped_session(sessionmaker(bind=engine))


@app.route('/ping', methods=['GET'])
def api_ping(*args, **kwargs):
    resp = "Cats Service. Version 0.1"
    return resp


@app.route('/cats', methods=['GET'])
def api_cats(*args, **kwargs):
    _attribute = request.args.get('attribute', '1')
    _order = request.args.get('order', 'ASC')
    _offset = request.args.get('offset', '0')
    _limit = request.args.get('limit', 'ALL')
    resp = db.execute("""SELECT * FROM cats ORDER BY %s %s LIMIT %s OFFSET %s""" % (_attribute, _order, _limit, _offset)).fetchall()
    return json.dumps([dict(r) for r in resp])


@app.route('/cat', methods=['POST'])
def api_add_cat(*args, **kwargs):
    if request.method == 'POST':
        cat_dict = request.get_json(force=True)
        db.execute("""INSERT INTO cats (name, color, tail_length, whiskers_length)
                          VALUES (:name, :color, :tail_length, :whiskers_length)""", cat_dict)
        return "Everything just fine."


if __name__ == '__main__':
    os.environ['FLASK_APP'] = 'application.py'
    os.environ['FLASK_DEBUG'] = '1'
    if platform.system() == 'Linux':
        os.system(f'sudo flask run --no-reload')
    elif platform.system() == 'Windows':
        os.system(f'flask run --no-reload')
