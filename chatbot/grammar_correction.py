from gramformer import Gramformer
import torch
import spacy
import random
from thefuzz import fuzz

class GrammarModel(Gramformer):
    """
    Grammar correction model.
    """
    def __init__(self, models=1, use_gpu=False, seed=1212):
        self.gm = super().__init__(models=1, use_gpu=False)
        self.ignore_errors = ['OTHER', 'ORTH']

    def grammar_correction(self,last_user_input):
        """
        Generate a corrected sentence and a message to the user with the correction.
        """
        corrected_sentence = self.correct(last_user_input, max_candidates=1)
        corrected_sentence = list(corrected_sentence)[0]
        message_styles = [
            "I think you meant: ",
            "Oh, you mean: ",
            "This would be better said like this: "
        ]

        if corrected_sentence != last_user_input:
            correction_message = f"{random.choice(message_styles)} \"{corrected_sentence}\" "
        else:
             correction_message = None

        return corrected_sentence, correction_message


    def add_correction_to_chat_history(self, chat_history):
        """
        Append the message to the user to the chat history.
        Return the corrected sentence.
        """
        last_user_input = chat_history.get_last_message_text()
        corrected_sentence, correction_message = self.grammar_correction(last_user_input)
        error_types = self.get_edits(last_user_input, corrected_sentence)
        relevant_error = any(error not in self.ignore_errors for error in error_types) # check if there is an error in the sentence which is not in the ignore list 
        token_sort_ratio = fuzz.token_sort_ratio(corrected_sentence, last_user_input) # calculate token similarity (ignoring punctuation and casing)
        
        if correction_message and relevant_error and token_sort_ratio != 100:
            chat_history.add_bot_message(text=correction_message, correction=True)
        
        return chat_history      


    def _get_edits(self, input_sentence, corrected_sentence):
        """
        Return the type of the error.
        """
        input_sentence = self.annotator.parse(input_sentence)
        corrected_sentence = self.annotator.parse(corrected_sentence)
        alignment = self.annotator.align(input_sentence, corrected_sentence)
        edits = self.annotator.merge(alignment)

        if len(edits) == 0:  
            return []

        edit_annotations = []
        for e in edits:
            e = self.annotator.classify(e)
            edit_annotations.append(e.type[2:])
                
        if len(edit_annotations) > 0:
            return edit_annotations
        else:    
            return []