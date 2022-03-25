import os
import tempfile

import pytest
from chatbot import create_app
from chatbot.db import get_db, init_db

# Load SQL command to create test database
with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


def pytest_generate_tests(metafunc):
    """ Overwrite some test environment variables """
    os.environ['OPENAI_ENGINE']='ada'

@pytest.fixture
def app():
    """ Create application instance for testing """
    # Create and open temp file
    # Returns file descriptor and path
    db_fd, db_path = tempfile.mkstemp()

    # Create app in test mode
    # and set test file as database
    app = create_app(test_config={
        'TESTING': True,
        'DATABASE': db_path,
        'LOAD_GRAMMAR_MODEL': False
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    # del(app.language_model)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """ Create client for tests """
    return app.test_client()

@pytest.fixture
def runner(app):
    """ Create a cli runner to call click commands """
    return app.test_cli_runner()


class AuthActions(object):
    """ Class to perform common auth operations for testing """
    def __init__(self, client):
        self._client = client

    def login(self, email='test@test.com', password='test'):
        """ Login as a user called 'test' """
        return self._client.post(
            '/auth/login',
            data={'email': email, 'password': password}
        )
    
    def logout(self):
        """ Logout """
        return self._client.get('/auth/logout')

# Register the auth actions
# Can now be called in test
# Example: auth.login()
@pytest.fixture
def auth(client):
    return AuthActions(client)