#! /usr/bin/python3
#! -*- coding: utf-8 -*-


import json
import os
import platform
from flask import Flask, jsonify, render_template, make_response, request
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
os.environ['DATABASE_URL'] = 'postgres://localhost:5432/'
engine = create_engine(os.getenv('DATABASE_URL'))
db = scoped_session(sessionmaker(bind=engine))


@app.route('/')
def index():
    print('Hello world!')
    return make_response()


@app.route('/ping')
def api_ping(methods=['GET'], *args, **kwargs):
    return "Cats Service. Version 0.1"


if __name__ == '__main__':
    os.environ['FLASK_APP'] = 'application.py'
    os.environ['FLASK_DEBUG'] = '1'
    if platform.system() == 'Linux':
        os.system(f'sudo flask run --no-reload')
    elif platform.system() == 'Windows':
        os.system(f'flask run --no-reload')
