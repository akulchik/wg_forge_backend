#! /usr/bin/python3
#! -*- coding: utf-8 -*-


import json
import os
import platform
import werkzeug.exceptions as ex
import wg_forge_api_schemas as _schemas
from flask import Flask, abort, g, make_response, request
from flask_expects_json import expects_json
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Enable ORM.
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


# Initialize and configure the application.
app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=['600 per minute']
)

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
@expects_json(_schemas.CAT_SCHEMA, force=True)
def api_add_cat(*args, **kwargs):
    cat_dict = g.data
    db_cols = db.execute("""SELECT column_name
                                FROM information_schema.columns
                                WHERE table_name='cats'""").fetchall()
    column_names = [r[0] for r in db_cols]

    for k in cat_dict.keys():
        if k not in column_names:
            return abort(404)

    _name = cat_dict.get('name')
    if _name is None:
        return abort(404)

    _color = cat_dict.get('color')
    if _color is None:
        return abort(404)

    _tail_length = cat_dict.get('tail_length')
    if _tail_length is None:
        return abort(404)
    elif type(_tail_length) is not int:
        return abort(404)
    elif _tail_length < 0:
        return abort(404)

    _whiskers_length = cat_dict.get('whiskers_length')
    if _whiskers_length is None:
        return abort(404)
    elif type(_whiskers_length) is not int:
        return abort(404)
    elif _whiskers_length < 0:
        return abort(404)

    #db.execute("""INSERT INTO cats (name, color, tail_length, whiskers_length)
    #                 VALUES (:name, :color, :tail_length, :whiskers_length)""", cat_dict)
    return 'It still works.'


if __name__ == '__main__':
    os.environ['FLASK_APP'] = 'application.py'
    os.environ['FLASK_DEBUG'] = '1'
    if platform.system() == 'Linux':
        os.system('sudo flask run --no-reload')
    elif platform.system() == 'Windows':
        os.system('flask run --no-reload')
