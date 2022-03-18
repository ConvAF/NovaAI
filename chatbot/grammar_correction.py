from gramformer import Gramformer
import torch
import spacy
import random

class GrammarModel(Gramformer):
    """
    Grammar correction model.
    """
    def __init__(self, models=1, use_gpu=False, seed=1212):
        self.gf = super().__init__(models=1, use_gpu=False)
        self.seed = seed
        set_seed(self.seed)


    def set_seed(self, seed):
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)


    def grammar_correction(self, user_input):
        """
        Generate a corrected sentence and a message to the user with the correction.
        """

        corrected_sentence = self.correct(user_input, max_candidates=1)
        corrected_sentence = list(corrected_sentence)[0]

        if corrected_sentence != user_input:
            correction_message = f"[Correction] {corrected_sentence}"
            print(correction_message)

        return corrected_sentence, correction_message


    def add_correction_to_chat_history(self, chat_history):
        """
        Append the message to the user to the chat history.
        Return the corrected sentence.
        """
        pass

    def _get_edits(self, user_input, corrected_sentence):
        user_input = self.annotator.parse(user_input)
        corrected_sentence = self.annotator.parse(corrected_sentence)
        alignment = self.annotator.align(user_input, corrected_sentence)
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