import pytest
import copy
from flask import session
from chatbot.db import get_db
from chatbot.grammar_correction import GrammarModel
from chatbot.utils import get_empty_chat_history

  
def test_grammar_correction_model_response(app):
    """ Test the responses of the grammar correction model """
    # Load language model (not loaded in test app by default)
    app.grammar_correction = GrammarModel(models = 1, use_gpu=False)

    # Language model is loaded
    assert app.grammar_correction

    # test Variables
    test_input_sentence = "Thanks you."
    test_corrected_sentence = "Thank you."

    # Grammar correction
    corrected_sentence, correction_message = app.grammar_correction.grammar_correction(test_input_sentence)
    assert corrected_sentence != test_input_sentence
    assert correction_message != None

    # A valid response is created for each history
    # 1. The sentence is correct (no correction).
    # chat_history_correct = [{'sender': 'User', 'text': 'Thank you.'}]
    chat_history_correct = get_empty_chat_history()
    chat_history_correct.add_user_message("Thank you.")
    chat_history_correct_old = copy.deepcopy(chat_history_correct)
    chat_history_response_correct = app.grammar_correction.add_correction_to_chat_history(chat_history_correct)
    # The chat history has not increased (no correction)
    assert len(chat_history_response_correct.messages) == len(chat_history_correct_old.messages)

    # 2. The sentence is incorrect (correction).
    # chat_history_incorrect = [{'sender': 'User', 'text': 'After he go to school, he walk home'}]
    chat_history_incorrect = get_empty_chat_history()
    chat_history_incorrect.add_user_message('After he go to school, he walk home')
    # chat_history_incorrect_old = chat_history_incorrect.copy()
    chat_history_incorrect_old = copy.deepcopy(chat_history_incorrect)
    chat_history_response_incorrect = app.grammar_correction.add_correction_to_chat_history(chat_history_incorrect)
    # The chat history has increased by 1 (correction)
    assert len(chat_history_response_incorrect.messages) == len(chat_history_incorrect_old.messages) + 1

    # In case of error, an error type is returned.s

    error_type = app.grammar_correction._get_edits(test_input_sentence, test_corrected_sentence)
    assert len(error_type) != 0
