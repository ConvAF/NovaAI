import pytest
from flask import g, session
from chatbot.db import get_db

def test_register(client, app):
    """ Test whether registration works """
    # Test GET method for view
    assert client.get('/auth/register').status_code == 200
    # Test POST method
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
    )
    # Test redirect to login url
    assert 'http://localhost/auth/login' == response.headers['Location']
    # Test user has been added to database
    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None

@pytest.mark.parametrize(
    ('username', 'password', 'message'), (
        ('', '', b'Username is required.'),
        ('a', '', b'Password is required.'),
        ('test', 'test', b'User test is already registered.')
    )
)
def test_register_validate_input(client, username, password, message):
    """ Test responses for different register input """
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    # Note: response data is in bytes
    assert message in response.data


def test_login(client, auth):
    """ Test whether login works """
    # Test GET method for view
    assert client.get('/auth/login').status_code == 200
    # Test POST method
    response = auth.login()
    # Test redirect for root
    assert response.headers['Location'] == 'http://localhost/'

    # Check that user is logged in in sessino
    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(
    ('username', 'password', 'message'), (
        ('a', 'test', b'User not found.'),
        ('test', 'a', b'Incorrect password.'),
    )
)
def test_login_validate_input(auth, username, password, message):
    """ Test respsonses for different login input """
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    """ Test logout """
    auth.login()

    with client:
        auth.logout()
        # Client should not be in session after logout
        assert 'user_id' not in session