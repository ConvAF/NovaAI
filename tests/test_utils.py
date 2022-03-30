# from this import d
import pytest
# from flask import session
# from chatbot.db import get_db
# from chatbot.language_model import LanguageModel
from chatbot.chat import ChatHistory
from chatbot.utils import get_simple_chat_history, print_chat_history

def test_print_chat_history():
    """ Test printing of the chat history """
    ch = get_simple_chat_history()
    print_chat_history(ch)
    
