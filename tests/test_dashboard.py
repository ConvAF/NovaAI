import pytest
from chatbot.db import get_db


def test_dashboard_view(client, auth):
    """ Test whether the view works """
    # Test GET
    # Not logged in request redirects to login
    response = client.get('/dashboard/')
    assert response.status_code == 302
    assert 'http://localhost/auth/login' == response.headers['Location']

    # If logged in, view is returned
    with client: # Inside app context
        # Logged in returns template
        auth.login()    

        response = client.get('/dashboard/')
        assert response.status_code == 200
