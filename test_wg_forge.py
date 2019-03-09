import pytest
from application import app
from flask import request, jsonify


@pytest.fixture
def client(request):
    test_client = app.test_client()

    def teardown():
        pass

    request.addfinalizer(teardown)
    return test_client


def test_dummy(client):
    response = client.get('/ping')
    assert b'Cats Service. Version 0.1' in response.data
