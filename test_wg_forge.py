import os
import tempfile
import pytest
import application as appl
from flask import request, jsonify


@pytest.fixture
def client():
    db_fd, appl.app.config['DATABASE'] = tempfile.mkstemp()
    appl.app.config['TESTING'] = True
    client = appl.app.test_client()

    with appl.app.app_context():
        appl.init_db()

    yield client

    os.close(db_fd)
    os.unlink(appl.app.config['DATABASE'])


def test_api_ping(client):
    """Start with a blank database."""
    rv = client.get('/ping')
    assert b'Cats Service. Version 0.1' in rv.data


def test_api_cats_case0(client):
    """Request with no parameters."""
    rv = client.get('/cats')
    assert rv.status_code == 200


def test_api_cats_case1(client):
    """Request with attribute."""
    rv = client.get('/cats?attribute=name')
    assert rv.status_code == 200, 'Valid attribute name'
    rv = client.get('/cats?attribute=imya')
    assert rv.status_code == 400, 'Invalid attribute name'


def test_api_cats_case2(client):
    """Request with order."""
    rv = client.get('/cats?order=desc')
    assert rv.status_code == 200, 'Valid order'
    rv = client.get('/cats?order=descending')
    assert rv.status_code == 400, 'Invalid order'


def test_api_cats_case3(client):
    """Request with limit."""
    rv = client.get('/cats?limit=4')
    assert rv.status_code == 200, 'Valid integer limit'
    rv = client.get('/cats?limit=all')
    assert rv.status_code == 200, 'Valid \'ALL\' limit'
    rv = client.get('/cats?limit=-7')
    assert rv.status_code == 400, 'Negative limit'
    rv = client.get('/cats?limit=vsevsevse')
    assert rv.status_code == 400, 'String limit'
    rv = client.get('/cats?limit=3.14')
    assert rv.status_code == 400, 'Floating point limit'


def test_api_cats_case4(client):
    """Request with offset."""
    rv = client.get('/cats?offset=4')
    assert rv.status_code == 200, 'Valid offset'
    rv = client.get('/cats?offset=-7')
    assert rv.status_code == 400, 'Negative offset'
    rv = client.get('/cats?offset=vsevsevse')
    assert rv.status_code == 400, 'Offset of string data type'
    rv = client.get('/cats?offset=3.14')
    assert rv.status_code == 400, 'Floating point offset'


def test_api_cats_case5(client):
    """Every parameter specified."""
    rv = client.get('/cats?attribute=color&order=asc&limit=15&offset=10')
    assert rv.status_code == 200, 'Every parameter specified'


def test_api_cats_case6(client):
    """Too many request parameters."""
    rv = client.get('/cats?attribute=color&order=asc&limit=15&offset=10&wrongparameter=wrongvalue')
    assert rv.status_code == 400, 'Too many parameters'
