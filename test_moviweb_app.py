import pytest
from moviweb_app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data == b"Welcome to MovieWeb App!"


def test_list_users(client):
    response = client.get('/users')
    assert response.status_code == 200
    # Add assertions to check the response content


def test_user_movies(client):
    response = client.get('/users/1')
    assert response.status_code == 200


if __name__ == '__main__':
    pytest.main()
