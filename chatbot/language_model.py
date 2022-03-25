import os
import openai

ENGINES = {
    'ada': 'text-ada-001',
    'babbage': 'text-babbage-001',
    'curie': 'text-curie-001',
    'davinci': 'text-davinci-002'
}


PROMPT_BASES = {
    'general_chat': "The following is a conversation with an AI Language Teacher called Artemis. Artemis is helpful, funny, very friendly, and very good at teaching English. Artemis helps users to practice English by having conversations.",
    'general_chat_easy': "In this conversation, the AI Teacher is discussing everyday topics with the student. Examples of topics are: greetings, introducing each other, telling time, talking about family and hobbies, counting. The teacher uses beginner level English. The conversation is made with short and simple sentences. After each interaction, the AI Teacher asks a new question.\nTeacher: Tell me, what would you like to talk about today?\nStudent: What do you suggest?",
    'general_chat_intermediate': "In this conversation, the AI Teacher is discussing everyday topics with the student. The teacher uses intermediate level English. It sometimes asks hypothetical questions to the student and uses present, past and future tenses. After each interaction, the AI Teacher asks a new question.\Teacher: Tell me, what would you like to talk about today?\nStudent: What do you suggest?",
    'general_chat_advanced': "In the following exchange, the AI Teacher is having a casual conversation with the student. The teacher uses high-level complex academic English. The AI Teacher talks in long sentences and uses uncommon words and synonyms. It sometimes asks hypothetical questions to the student and uses present, past and future tenses. The AI Teacher asks the student for his opinion on complex topics such as personal values, metaphysical questions, religion, current affairs, etc. After each interaction, the AI Teacher asks a new question.\nTeacher: Tell me, what would you like to talk about today?",
    'situation_bakery': "The following is a conversation with Lola the baker. Lola is helpful, clever, and very friendly.\nHuman: Good morning!\nLola: Hello, how can I help you?",
    'situation_store': "The following is a conversation between a Human and a store clerk called Artemis. The conversation takes place at a store. The Human needs help finding some items in the store as well as the price of those items. Artemis helps him out.\nArtemis: Hi, my name is Artemis. May I help you?",
    'situation_restaurant': "The following is a conversation between a waiter named Artemis and a client. The interaction takes place in a restaurant at lunch time. Artemis is helpful clever, and very friendly. He wants to make sure the client has a nice experience at the restaurant. \nArtemis: Hello my name is Artemis, I'll be your waiter today."
}

class LanguageModel():
    """ Language Generation Model
    """
    def __init__(self, 
            prompt_context='general_chat',
            ):

        # Init openai
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.engine = os.getenv("OPENAI_ENGINE")
        self.temperature = 0.5

        # Set context
        assert prompt_context in PROMPT_BASES.keys()
        self.prompt_base = PROMPT_BASES[prompt_context]



    def add_response_to_chat_history(self, chat_history):
        """ Generate a response from the bot and append to chat history.
        
        Converts the chat history to a flat string of ids,
        and generates a prediction from the Blenderbot model.
        """
        if chat_history is None or len(chat_history)==0:
            return chat_history
        

        reply_text = self.get_response_from_GPT3(chat_history)

        if reply_text:
            chat_history.append(
                {
                    'sender': 'bot',
                    'text': reply_text
                }
            )
        return chat_history

    def get_response_from_GPT3(self, chat_history):
        """ Get a reply from GPT3 
        
        Returns:
        --------
         - reply: str
            A text string containing just the reply from the model.
            Example: "I'm fine, how are you?"
        """
        prompt = self.create_prompt(chat_history)

        response = openai.Completion.create(
                engine=self.engine,
                prompt=prompt,
                temperature=self.temperature,
            )

        reply = None
        if response and ('choices' in response) and len(response['choices']):

            reply_raw = response['choices'][0]['text']
            reply = self.clean_reply_text(reply_raw)

        return reply

    def clean_reply_text(self, reply_raw):
        " Clean up the reply reply_raw a bit "

        reply = reply_raw.strip()
        # Get rid of "Bot: " at beginning of message
        reply = ":".join(reply.split(':')[1:]).strip()

        # Sometimes, a partial reply of a user is included. Remove that
        # Example: "Bot: Hello, how are you? User: "
        if 'User:' in reply:
            idx = reply.find('User:')
            reply = reply[:idx].strip()

        return reply
        

    def create_prompt(self, chat_history):
        """ Convert the recent chat history to a prompt for GPT-3.
        
        Combines the base prompt and the recent chat history
        to a prompt for GPT3 to create the next sentence.
        """

        prompt_base = self.prompt_base

        # Limit the chat_history to the past 100 messages
        chat_history = chat_history[-100:]
        # Exclude messages that have a correction
        prompt_conv = "\n".join([f"{message['sender'].title()}: {message['text']}" for message in chat_history
                                 if not ('correction' in message.keys())])

        prompt = "\n".join([prompt_base, prompt_conv])
        return prompt