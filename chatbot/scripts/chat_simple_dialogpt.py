import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from transformers import AutoModelWithLMHead, AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM
import torch


def load_tokenizer_and_model(model="microsoft/DialoGPT-large"):
    """
    Load tokenizer and model instance for some specific DialoGPT model.
    """
    # Initialize tokenizer and model
    print("Loading model...")
    tokenizer = AutoTokenizer.from_pretrained(model)
    model = AutoModelForCausalLM.from_pretrained(model)

    # Return tokenizer and model
    return tokenizer, model


def generate_response(tokenizer, model, chat_round, chat_history_ids):
    """ Generate a response to user input
    """
    # Get user input and EOS token
    new_user_input_ids = tokenizer.encode(input(">> User: ") + tokenizer.eos_token, return_tensors='pt')

    # Append to chat history
    bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1)\
        if chat_round>0 else new_user_input_ids
    
    # Generate response given maximum chat length history of 1250 tokens(?)
    chat_history_ids = model.generate(bot_input_ids, max_length=1250, pad_token_id=tokenizer.eos_token_id)

    # Pretty print out tokens from the bot
    print(">> DialoGPT: {}".format(tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)))

    return chat_history_ids

def chat_for_n_rounds(n=5):
    """ Chat with the chatbot for n rounds
    """

    # Initialize tokenizer and model
    tokenizer, model = load_tokenizer_and_model()

    # Initialize history variable
    chat_history_ids = None
    
    # Chat for n rounds
    for chat_round in range(n):
        chat_history_ids = generate_response(tokenizer, model, chat_round, chat_history_ids)


if __name__ == "__main__":
    chat_for_n_rounds(5)