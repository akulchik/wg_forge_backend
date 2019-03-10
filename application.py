#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import wg_forge_api as _api
import wg_forge_api_exceptions as _exc
import wg_forge_api_schemas as _schemas
import wg_forge_api_queries as _q
from flask import Flask, abort, g, jsonify, request
from flask_expects_json import expects_json
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


# Initialize and configure the application.
app = Flask(__name__)

# Set requests limit to 600 times per minute.
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=['600 per minute']
)


def init_db():
    os.environ['DATABASE_URL'] = 'postgresql://wg_forge:a42@localhost:5432/wg_forge_db'
    engine = create_engine(os.getenv('DATABASE_URL'))
    db = scoped_session(sessionmaker(bind=engine))


# Set up database and database engine.
os.environ['DATABASE_URL'] = 'postgresql://wg_forge:a42@localhost:5432/wg_forge_db'
engine = create_engine(os.getenv('DATABASE_URL'))
db = scoped_session(sessionmaker(bind=engine))


@app.route('/ping', methods=['GET'])
def api_ping(*args, **kwargs):
    """
    Returns heartbeat string with service information.
    :param args: Unexpected arguments.
    :param kwargs: Unexpected keyword arguments.
    :return: status code 200 - ok.
    """
    resp = "Cats Service. Version 0.1"
    return resp, 200


@app.route('/cats', methods=['GET'])
def api_cats(*args, **kwargs):
    """
    Query database to retrieve data about cats.
    :param args: Unexpected arguments.
    :param kwargs: Unexpected keyword arguments.
    :return: status code 200 - JSON with requested information.
    :return: status code 400 - invalid request parameters.
    """
    try:
        cat_dict = request.args
        _api.validate_cats_select_parameters(cat_dict)
        attribute = cat_dict.get('attribute', '1')
        order = cat_dict.get('order', 'ASC')
        limit = cat_dict.get('limit', 'ALL')
        offset = cat_dict.get('offset', '0')
        resp = db.execute(_q.select_cats_query.format(attribute, order, limit, offset)).fetchall()
        return jsonify([dict(r) for r in resp]), 200
    except _exc.TooManyParameters as e:
        return abort(400, e.description)
    except _exc.UnexpectedParameter as e:
        return abort(400, e.description)
    except _exc.UnexpectedParameterValue as e:
        return abort(400, e.description)


@app.route('/cat', methods=['POST'])
@expects_json(_schemas.CAT_SCHEMA, force=True)
def add_cat(*args, **kwargs):
    """
    Update database with a new cat.
    :param args: Unexpected arguments.
    :param kwargs: Unexpected keyword arguments.
    :return: status code 201 - database updated.
    :return: status code 400 - bad JSON data.
    """
    try:
        cat_dict = g.data
        _api.validate_no_extra_parameters(cat_dict)
        _api.validate_cat_tail_and_whiskers(cat_dict)
        #db.execute(_q.insert_cat_query, cat_dict)
        resp = 'Database successfully updated.'
        return resp, 201
    except _exc.TailLengthIsNegative as e:
        return abort(400, e.description)
    except _exc.TooManyParameters as e:
        return abort(400, e.description)
    except _exc.WhiskersLengthIsNegative as e:
        return abort(400, e.description)


app.run(debug=True, port=8080, use_reloader=False)
