import pytest
from flask import g, session
from chatbot.db import get_db


def test_register(client, app):
    """ Test whether registration works """
    # Test GET
    # View is returned
    assert client.get('/auth/register').status_code == 200
    # Test POST
    # Registration succeeds
    response = client.post(
        '/auth/register', data={'name': 'a', 'email': 'a@a.com', 'password': 'a'}
    )
    # Successful registration redirects to login
    assert response.headers['Location'] in 'http://localhost/auth/login?sign_up_success=True'
    # Test user has been added to database
    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE email = 'a@a.com'",
        ).fetchone() is not None
    # app.teardown_appcontext()

@pytest.mark.parametrize(
    ('name', 'email', 'password', 'message'), (
        ('', '', '', b'Name is required.'),
        ('a', '', '', b'Email is required.'),
        ('a', 'a', '', b'Password is required.'),
        ('test', 'test@test.com', 'test', b'User with Email test@test.com is already registered.')
    )
)
def test_register_validate_input(client, name, email, password, message):
    """ Test responses for different register input """
    response = client.post(
        '/auth/register',
        data={'name': name, 'email': email, 'password': password}
    )
    # Note: response data is in bytes
    assert message in response.data

def test_login(client, auth):
    """ Test whether login works """
    # GET
    # View is returned
    assert client.get('/auth/login').status_code == 200

    # View is returned after signup
    response = client.get('/auth/login?sign_up_success=True')
    assert response.status_code == 200
    assert b'Success! You can now log in.' in response.data

    # POST
    # Login succeeds
    response = auth.login()
    # Login redirects the user to root
    assert response.headers['Location'] in 'http://localhost/dashboard/'

    # After login, user is logged in in session
    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['email'] == 'test@test.com'
    
    # After login, login screen redirects to dashboard
    with client:
        response = client.get('/auth/login')
        assert response.headers['Location'] in 'http://localhost/dashboard/'


@pytest.mark.parametrize(
    ('email', 'password', 'message'), (
        ('asdf@asdf.com', 'test', b'No user with Email asdf@asdf.com found'),
        ('test@test.com', 'a', b'Incorrect password'),
    )
)
def test_login_validate_input(auth, email, password, message):
    """ Test responses for different login input """
    response = auth.login(email, password)
    assert message in response.data


def test_logout(client, auth):
    """ Test logout """
    auth.login()

    with client:
        auth.logout()
        # User is logged out after logout
        assert 'user_id' not in session

def test_login_required(client, auth):
    """ Test that login is required for protected views """
    # Test redirect to login url
    with client:
        response = client.get('/chat/general_chat_beginner')
        assert response.status_code == 302 # Redirect has occured
        assert response.headers['Location'] in 'http://localhost/auth/login'
    
    # Now logged in
    auth.login()
    with client:
        response = client.get('/chat/general_chat_beginner')
        assert response.status_code == 200 # No redirect

