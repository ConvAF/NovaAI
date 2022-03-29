# from this import d
import pytest
# from flask import session
# from chatbot.db import get_db
# from chatbot.language_model import LanguageModel
from chatbot.chat import ChatHistory
from chatbot.utils import get_simple_chat_history


@pytest.mark.parametrize(
    ('reply_raw', 'reply_clean_target'), (
        ('Bot: Hello! This is my answer.', 'Hello! This is my answer.'),
        ('Bot: Hello! This is my answer. User: The user answer is included', 'Hello! This is my answer.'),
        ('\nBot:\n Hello! This is my answer.\n\n', 'Hello! This is my answer.'),
    )
)
def test_reply_cleaning(app, reply_raw, reply_clean_target):
    """ Test the cleaning of replies by the language model """
    tag_bot = "Bot"
    tag_user = "User"
    with app.app_context():
        reply_clean = app.language_model.clean_reply_text(reply_raw, tag_bot, tag_user)
        assert reply_clean == reply_clean_target


def test_language_model_OpenAI_parsing(app):
    """ Tests whether the language model can contact OpenAI and get a response"""
    # app.language_model = LanguageModel()
    chat_history = get_simple_chat_history()
    with app.app_context():
        reply = app.language_model.get_response_from_GPT3(chat_history)
        assert(reply)
        # import sys
        # print(response, file=sys.stdout)


def test_language_model_response(app):
    """ Test the responses of the language model """
    # Load language model (not loaded in test app by default)
    # app.language_model = LanguageModel()

    # Language model is loaded
    assert app.language_model

    # Empty history returns empty history

    # chat_history = []
    # chat_history_response = app.language_model.add_response_to_chat_history(chat_history, prompt_text="Dummy text.")
    # assert len(chat_history_response)==0

    # A valid response is created for each history
    with app.app_context():
 
        chat_history = ChatHistory(prompt_base = "The following is a conversation between a Bot and a User.", tag_bot = "Bot", tag_user = "User")
        chat_history.add_user_message("Hello bot, how are you?")

        n_messages_old = len(chat_history.messages)
        assert n_messages_old == 1
        chat_history = app.language_model.add_response_to_chat_history(chat_history)
        n_messages_new = len(chat_history.messages)
        # import sys
        # print("-----------------\nChat History\n\n", chat_history, file=sys.stdout)
        # print(f"-----------------\nChat History\n\n{chat_history.get_as_prompt_with_dialog()}", file=sys.stdout)
        
        # The chat history has increase by one
        assert n_messages_new == 2



