import os
import tempfile

import pytest

from main import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['DATABASE_NAME'] = 'mydb_test'

    with app.test_client() as client:
        yield client


def test_user_list_return_ok():
    response = client.get('/api/v1/users')

    assert response.status == 200
    assert len(response) == 2


def test_create_user_anonymous_return_permission_denied():
    response = client.post(
        '/api/v1/users', json={'username': 'pepe'})

    assert response.status == 403


def test_create_user_authenticated_return_ok():
    response = client.post(
        '/api/v1/users',
        json={'username': 'pepe'},
        headers={'Authorization': 'Bearer hola'}
    )

    assert response.status == 200


def test_update_user_anonymous_return_permission_denied():
    response = client.put(
        '/api/v1/users/1', json={'username': 'pepe'})

    assert response.status == 403


def test_update_user_authenticated_return_notfound():
    response = client.put(
        '/api/v1/users/999',
        json={'username': 'pepe'},
        headers={'Authorization': 'Bearer hola'}
    )

    assert response.status == 404


def test_update_user_authenticated_return_ok():
    response = client.put(
        '/api/v1/users/1',
        json={'username': 'pepe'},
        headers={'Authorization': 'Bearer hola'}
    )

    assert response.status == 200


def test_delete_user_anonymous_return_permission_denied():
    response = client.delete('/api/v1/users/1')

    assert response.status == 403


def test_delete_user_authenticated_return_notfound():
    response = client.delete(
        '/api/v1/users/999',
        headers={'Authorization': 'Bearer hola'}
    )

    assert response.status == 404


def test_delete_user_authenticated_return_ok():
    response = client.delete(
        '/api/v1/users/1',
        headers={'Authorization': 'Bearer hola'}
    )

    assert response.status == 204
