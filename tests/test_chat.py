import pytest
from flask import session
from chatbot.language_model import LanguageModel
from chatbot.grammar_correction import GrammarModel

def test_chat_general(client, auth, app):
    """ Test whether general chat functionality works works """
    
    # Load language model (not loaded in test app by default)
    app.language_model = LanguageModel()
    app.grammar_correction = GrammarModel(models = 1, use_gpu=False)

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


def test_chat_send_message(client, auth, app):
    """ Test the chat functionality """

    # Load language model (not loaded in test app by default)
    app.language_model = LanguageModel()
    app.grammar_correction = GrammarModel(models = 1, use_gpu=False)

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


def test_clear_chat_history(client, auth, app):
    """ Test the clear chat functionality """

    # Load language model (not loaded in test app by default)
    app.language_model = LanguageModel()
    app.grammar_correction = GrammarModel(models = 1, use_gpu=False)

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