import pytest
from flask import session
from chatbot.language_model import LanguageModel
from chatbot.grammar_correction import GrammarModel
from chatbot.chat import ChatMessage, ChatHistory

CHAT_VALID_ENDPOINT = 'general_chat_beginner'

def test_chat_overview(client, auth, app):
    """ Test the chat overview page """
    # Test GET
    # Not logged in request redirects to login
    response = client.get('/chat/')
    assert response.status_code == 302
    assert response.headers['Location'] in 'http://localhost/auth/login'
    

    with client: # Inside app context
        # Logged in returns template
        auth.login()    
        response = client.get('/chat/')
        assert response.status_code == 200



def test_chat(client, auth, app):
    """ Test whether general chat functionality works works """
    
    # Load language model (not loaded in test app by default)
    app.config['LOAD_GRAMMAR_MODEL'] = True # Only then used
    app.language_model = LanguageModel()
    app.grammar_correction = GrammarModel(models = 1, use_gpu=False)
    # Test GET
    # Not logged in request redirects to login
    response = client.get('/chat/test')
    assert response.status_code == 302
    assert response.headers['Location'] in 'http://localhost/auth/login'
    
    with client: # Inside app context
        # Logged in returns template
        auth.login()    

        # Test a scenario that works
        response = client.get(f'/chat/{CHAT_VALID_ENDPOINT}')
        assert response.status_code == 200

        # Test a scenario that does not exists
        response = client.get('/chat/does_not_exists')
        assert response.status_code == 404

        # Chat history is empty on start
        assert session.get('chat_history') is None


# def test_chat_general(client, auth, app):
#     """ Test whether general chat functionality works works """
    
#     # Load language model (not loaded in test app by default)
#     app.config['LOAD_GRAMMAR_MODEL'] = True # Only then used
#     app.language_model = LanguageModel()
#     app.grammar_correction = GrammarModel(models = 1, use_gpu=False)
#     # Test GET
#     # Not logged in request redirects to login
#     response = client.get('/chat/general')
#     assert response.status_code == 302
#     assert 'http://localhost/auth/login' == response.headers['Location']
    

#     with client: # Inside app context
#         # Logged in returns template
#         auth.login()    

#         response = client.get('/chat/general')
#         assert response.status_code == 200

#         # Chat history is empty on start
#         assert session.get('chat_history') is None

        # Chat history has been initialized


def test_chat_send_message(client, auth, app):
    """ Test the chat functionality """

    # Load language model (not loaded in test app by default)
    app.language_model = LanguageModel()
    app.grammar_correction = GrammarModel(models = 1, use_gpu=False)

    with client:
        auth.login()
        response = client.post(
            f'/chat/{CHAT_VALID_ENDPOINT}',
            data={
                'text_input': 'Test message',
                'submit_button': 'Send'
                }
        )
        assert response.status_code == 200

        # Check that chat history has been created
        # assert session.get('chat_history')

        # Parse the endpoint again from saime location. Check that chat history has been retained
        response = client.get(f'/chat/{CHAT_VALID_ENDPOINT}', 
                                headers={'referrer': f'/chat/{CHAT_VALID_ENDPOINT}'})
        # assert session.get('chat_history')

        # Invalid form submission creates error
        response = client.post(
            f'/chat/{CHAT_VALID_ENDPOINT}',
            data={
                'text_input': 'a',
                'submit_button': 'Send'
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
        f'/chat/{CHAT_VALID_ENDPOINT}',
        data={
            'text_input': 'Test message',
            'submit_button': 'Send'
            }
        )
        # Asset chat history is full
        assert session.get('chat_history')
        # Clear chat history
        response = client.post(
            f'/chat/{CHAT_VALID_ENDPOINT}',
            data={
                'text_input': 'Test message',
                'submit_button': 'Clear chat'
                }
        )
        # Check that it is clear
        assert session.get('chat_history') is None
        # Clear the clear one again, does nothing
        response = client.post(
            f'/chat/{CHAT_VALID_ENDPOINT}',
            data={
                'text_input': 'Test message',
                'submit_button': 'Clear chat'
                }
        )


def test_chat_message_class():
    """ Test the chat message class """
    cm = ChatMessage(sender='user', text='Dummy message')
    cm.__repr__()
    js = cm.toJSON()
    cm = ChatMessage.fromJSON(js)

#TODO: Test chat history class