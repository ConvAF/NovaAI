from gramformer import Gramformer
import torch
import spacy
import random

class GrammarModel(Gramformer):
    """
    Grammar correction model.
    """
    def __init__(self, models=1, use_gpu=False, seed=1212):
        self.gm = super().__init__(models=1, use_gpu=False)


    def grammar_correction(self, chat_history):
        """
        Generate a corrected sentence and a message to the user with the correction.
        """

        corrected_sentence = self.correct(chat_history, max_candidates=1)
        corrected_sentence = list(corrected_sentence)[0]

        if corrected_sentence != chat_history:
            correction_message = f"[Correction] {corrected_sentence}"
            print(correction_message)

        return corrected_sentence, correction_message


    def add_correction_to_chat_history(self, chat_history):
        """
        Append the message to the user to the chat history.
        Return the corrected sentence.
        """
        corrected_sentence, correction_message = self.gm.grammar_correction(chat_history)
        error_types = self.gm.get_edits(chat_history, corrected_sentence)

         chat_history.append(
            {
                'sender': 'bot',
                'text': correction_message
            }
        )
        return chat_history       


    def _get_edits(self, chat_history, corrected_sentence):
        chat_history = self.annotator.parse(chat_history)
        corrected_sentence = self.annotator.parse(corrected_sentence)
        alignment = self.annotator.align(chat_history, corrected_sentence)
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