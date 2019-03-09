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


def test_ping(client):
    """Test whether the server is alive."""
    response = client.get('/ping')
    assert b'Cats Service. Version 0.1' in response.data


def post_json(client, url, json_dict):
    """Send dictionary json_dict as a json to the specified url."""
    return client.post(url, data=jsonify(json_dict), content_type='application/json')


def json_of_response(response):
    """Decode json from response."""
    return response.get_json()


def test_json(client, url, json_dict, json_expected):
    """Test JSON for POST endpoint."""
    response = post_json(client, url, json_dict)
    assert response.status_code == 200
    assert json_of_response(response) == json_expected
