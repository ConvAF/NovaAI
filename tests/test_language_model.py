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
    chat_history_response = app.language_model.add_response_to_chat_history(chat_history, prompt_text="Dummy text.")
    assert len(chat_history_response)==0

    # A valid response is created for each history
    with app.app_context():
        chat_history = [{'sender': 'User', 'text': 'Hello bot how are you?'}]
        chat_history_old = chat_history.copy()
        chat_history_response = app.language_model.add_response_to_chat_history(chat_history, prompt_text="This is a dummy prompt text.")
        # The chat history has increase by one
        assert len(chat_history_response) == len(chat_history_old) + 1


@pytest.mark.parametrize(
    ('chat_history', 'prompt_text'), (
        ([{'sender': 'user', 'text': 'Test'}], 'This is a dummy prompt text.'),
    )
)
def test_prompt_creation(app, chat_history, prompt_text):
    """ Test the creation of prompts """
    with app.app_context():
        app.language_model.create_prompt_with_dialog(chat_history, prompt_text)