import pytest
from flask.testing import FlaskClient
from moviweb_app import app


@pytest.fixture
def client() -> FlaskClient:
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_list_users(client):
    response = client.get('/users')
    assert response.status_code == 200
    assert b"Users" in response.data
    assert b"Alice" in response.data
    assert b"Bob" in response.data


def test_user_movies(client):
    response = client.get('/users/1')
    assert response.status_code == 200


def test_add_user(client):
    response = client.post('/add_user', data={'name': 'John'})
    assert response.status_code == 302  # Redirect


def test_add_movie(client):
    response = client.post('/users/1/add_movie', data={'title': 'The Matrix'})
    assert response.status_code == 302  # Redirect


def test_update_movie(client):
    response = client.post('/users/1/update_movie/1', data={'title': 'Inception 2.0'})
    assert response.status_code == 200  # Redirect


def test_delete_movie(client):
    response = client.get('/users/1/delete_movie/1')
    assert response.status_code == 302  # Redirect


if __name__ == '__main__':
    pytest.main()
