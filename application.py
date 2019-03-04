#! /usr/bin/python3
#! -*- coding: utf-8 -*-


import json
import os
from flask import Flask, jsonify, render_template, request
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
os.environ['DATABASE_URL'] = None
engine = create_engine(os.getenv('DATABASE_URL'))
db = scoped_session(sessionmaker(bind=engine))
