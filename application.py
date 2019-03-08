#! /usr/bin/python3
#! -*- coding: utf-8 -*-


import json
import os
import platform
import werkzeug.exceptions as ex
from flask import Flask, abort, render_template, make_response, request
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
    db_cols = db.execute("""SELECT column_name
                                FROM information_schema.columns
                                WHERE table_name='cats'""").fetchall()
    column_names = [r[0] for r in db_cols]

    _attribute = request.args.get('attribute', column_names[0])
    if _attribute not in column_names:
        return abort(404)

    _order = request.args.get('order', 'ASC')
    if _order.upper() not in ('ASC', 'DESC'):
        return abort(404)

    _offset = request.args.get('offset', '0')
    try:
        _offset = int(_offset)
        if _offset < 0:
            return abort(404)
    except ValueError:
        return abort(404)

    _limit = request.args.get('limit', 'ALL')
    try:
        if _limit.upper() != 'ALL':
            _limit = int(_limit)
            if _limit < 0:
                return abort(404)
    except ValueError:
        return abort(404)

    resp = db.execute("""SELECT *
                            FROM cats
                            ORDER BY %s %s
                            LIMIT %s
                            OFFSET %s""" % (_attribute, _order, _limit, _offset)).fetchall()
    return json.dumps([dict(r) for r in resp])


@app.route('/cat', methods=['POST'])
def api_add_cat(*args, **kwargs):
    if request.method == 'POST':
        cat_dict = request.get_json(force=True)
        db_cols = db.execute("""SELECT column_name
                                    FROM information_schema.columns
                                    WHERE table_name='cats'""").fetchall()
        column_names = [r[0] for r in db_cols]
        for k in cat_dict.keys():
            if k not in column_names:
                return abort(405)
        #db.execute("""INSERT INTO cats (name, color, tail_length, whiskers_length)
        #                 VALUES (:name, :color, :tail_length, :whiskers_length)""", cat_dict)
        return "Everything just fine."


if __name__ == '__main__':
    os.environ['FLASK_APP'] = 'application.py'
    os.environ['FLASK_DEBUG'] = '1'
    if platform.system() == 'Linux':
        os.system('sudo flask run --no-reload')
    elif platform.system() == 'Windows':
        os.system('flask run --no-reload')
