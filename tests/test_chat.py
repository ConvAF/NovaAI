import pytest
from flask import session
from chatbot.db import get_db

def test_chat(client, auth):
    """ Test whether general chat functionality works works """
    
    # Test GET
    # Not logged in request redirects to login
    response = client.get('/chat/general')
    assert response.status_code == 302
    assert 'http://localhost/auth/login' == response.headers['Location']
    

    with client: # Inside app context
        # Logged in returns template
        auth.login()    

        response = client.get('/chat/general')
        assert response.status_code == 200

        # Chat history is empty on start
        assert session.get('chat_history') is None

        # Chat history has been initialized


def test_chat_send_message(client, auth):
    """ Test the chat functionality """
    auth.login()
    response = client.post(
        '/chat/general',
        data={
            'text_input': 'Test message',
            'submit_button': 'Send text'
            }
    )
    assert response.status_code == 200

    # Invalid form submission creates error
    response = client.post(
        '/chat/general',
        data={
            'text_input': 'a',
            'submit_button': 'Send text'
            }
    )


def test_clear_chat_history(client, auth):
    """ Test the clear chat functionality """
    # Test that chat gets cleared on call
    with client:
        auth.login()
        # Fill chat history
        response = client.post(
        '/chat/general',
        data={
            'text_input': 'Test message',
            'submit_button': 'Send text'
            }
        )
        # Asset chat history is full
        assert session.get('chat_history')
        # Clear chat history
        response = client.post(
            '/chat/general',
            data={
                'text_input': 'Test message',
                'submit_button': 'Clear chat'
                }
        )
        # Check that it is clear
        assert session.get('chat_history') is None
        # Clear the clear one again, does nothing
        response = client.post(
            '/chat/general',
            data={
                'text_input': 'Test message',
                'submit_button': 'Clear chat'
                }
        )