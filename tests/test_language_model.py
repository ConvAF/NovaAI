import pytest
from flask import session
from chatbot.db import get_db
from chatbot.language_model import LanguageModel


def test_language_model_response(app):
    """ Test the responses of the language model """
    # Load language model (not loaded in test app by default)
    app.language_model = LanguageModel()

    # Language model is loaded
    assert app.language_model

    # Empty history returns empty history
    chat_history = []
    chat_history_response = app.language_model.add_response_to_chat_history(chat_history)
    assert len(chat_history_response)==0

    # A valid response is created for each history
    chat_history = [{'sender': 'User', 'text': 'Hello bot how are you?'}]
    chat_history_old = chat_history.copy()
    chat_history_response = app.language_model.add_response_to_chat_history(chat_history)
    # The chat history has increase by one
    assert len(chat_history_response) == len(chat_history_old) + 1