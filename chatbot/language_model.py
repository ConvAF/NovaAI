import torch
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration



class LanguageModel():
    """ Language Generation Model
    """
    def __init__(self):

        model_name = "facebook/blenderbot-400M-distill"

        self.tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
        self.model = BlenderbotForConditionalGeneration.from_pretrained(model_name)


    def add_response_to_chat_history(self, chat_history):
        """ """

        chat_history_ids = self.chat_history_to_ids(chat_history)

        reply_id = self.model.generate(chat_history_ids, max_length=1250)

        reply_text = self.tokenizer.decode(reply_id[0], skip_special_tokens=True).lstrip()

        chat_history.append(
            {
                'sender': 'bot',
                'text': reply_text
            }
        )
        return chat_history


    def chat_history_to_ids(self, chat_history):
        """ Convert the chat history to """
        texts = [message['text'] for message in chat_history]
        text_ids = [self.tokenizer.encode(text, return_tensors='pt') for text in texts]
        
        chat_history_ids = torch.cat(text_ids, dim=-1)

        return chat_history_ids
