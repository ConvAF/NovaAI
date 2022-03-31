"""
Chat views.
"""
from flask import Blueprint, render_template, request, session, current_app, abort
from wtforms import Form, StringField, validators
import json, copy
from random import choice

from chatbot.auth import login_required

# Create a blueprint for authentication
bp = Blueprint('chat', __name__, url_prefix='/chat')


@bp.route('/', methods=('GET',))
@login_required
def overview():
    """ Route for the chat overview
    """
    return render_template('chat/overview.html', prompts=current_app.prompts)


@bp.route('/<chat_scenario>', methods=('GET', 'POST'))
@login_required
def chat(chat_scenario):
    """ Route for chat with variable scenarios
    """
    form = ChatForm(request.form)

    # Return 404 if chat scenario not found
    promptExists = chat_scenario in current_app.prompts.keys()
    if not promptExists:
        abort(404)

    # If the users opens the chat from somewhere else, clear chat history
    userOpensChatFirstTime = request.url != request.referrer
    if userOpensChatFirstTime:
        clear_chat_history()

    prompt = current_app.prompts[chat_scenario]

    # Get chat history
    chat_history = session.get('chat_history')
    # Create if not exists
    if not chat_history:
        chat_history = ChatHistory(
                                    prompt_base = prompt['text'],
                                    tag_bot = prompt['tag_bot'],
                                    tag_user = prompt['tag_user'],
                                    initial_bot_messages_options = prompt.get('initial_bot_messages_options')
                                   )
    # On text form submission
    if request.method == 'POST':
        if request.form['submit_button'] == 'Clear chat':
            # Clear chat history
            clear_chat_history()
        elif request.form['submit_button'] == 'Send' and form.validate():
            # Add text to chat history
            chat_history.add_user_message(form.text_input.data)
            # Clear form
            form.text_input.data = ""
            # Get response from bot
            chat_history = get_bot_response(chat_history)
            # Update chat history
            session['chat_history'] = chat_history


    return render_template('chat/chat.html', 
                            # chat_scenario=chat_scenario,
                            prompt=prompt,
                            messages=chat_history.messages,
                            form=form,
                            loc = userOpensChatFirstTime
                            )


def get_bot_response(chat_history):
    """ Get response from the bot """

    if current_app.config['LOAD_GRAMMAR_MODEL']:
        # pass
        chat_history = current_app.grammar_correction.add_correction_to_chat_history(chat_history)
    chat_history = current_app.language_model.add_response_to_chat_history(chat_history)


    return chat_history

def clear_chat_history():
    """ Clear the chat history """
    if session.get('chat_history'):
        session.pop('chat_history')


class ChatMessage():

    def __init__(self,
                sender: str,
                text: str,
                correction: bool = False
                ):

        assert sender in ['user', 'bot']
        self.sender = sender
        self.text = text
        self.correction = correction

    def __repr__(self):
        return f"{self.sender}: {self.text}"
    
    def __copy__(self):
        return ChatMessage(
            sender=self.sender,
            text=self.text,
            correction=self.correction
        )

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    @staticmethod
    def fromJSON(obj_json):
        obj_dict = json.loads(obj_json)
        return ChatMessage(**obj_dict)


class ChatHistory():

    def __init__(self,
                    prompt_base,
                    tag_bot,
                    tag_user,
                    initial_bot_messages_options=None
                    ):

        self.prompt_base = prompt_base
        self.tag_bot = tag_bot
        self.tag_user = tag_user
        self.messages = []

        if initial_bot_messages_options:
            initial_message = choice(initial_bot_messages_options)
            self.add_bot_message(initial_message)


    def add_user_message(self, text: str):
        message = ChatMessage(sender='user', text=text)
        self.add_message(message)
    
    def add_bot_message(self, text: str, correction: bool=False):
        message = ChatMessage(sender='bot', text=text, correction=correction)
        self.add_message(message)

    def add_message(self, chat_message: ChatMessage):
        self.messages.append(chat_message)

    def get_last_message_text(self) -> ChatMessage:
        return self.messages[-1].text

    def get_as_prompt_with_dialog(self, limit_messages: int=10):
        """ Returns the chat history in a Dialog format

        Pattern is:
        prompt_base

        tag_user: message.text
        tag_bot: message.text
        etc.
        """
        messages = self.messages[-limit_messages:]
        # Exclude messages that have a correction
        dialog = "\n".join(
            [f"{self.format_sender_tag(message.sender)}: {message.text}"
                for message in messages
                if not message.correction
            ])
        # Add a final prompt for the (ie. "Bot:")
        dialog += f"\nf{self.tag_bot}:"

        prompt_with_dialog = "\n".join([self.prompt_base, dialog]).lstrip()
        return prompt_with_dialog


    def format_sender_tag(self, sender):
        if sender=='bot':
            return self.tag_bot.title()
        if sender=='user':
            return self.tag_user.title()

    def __len__(self):
        return len(self.messages)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def __repr__(self):
        return self.toJSON()

    def __copy__(self):
        chnew = ChatHistory(
                prompt_base=self.prompt_base,
                tag_bot=self.tag_bot,
                tag_user=self.tag_user,
                # initial_bot_messages_options=self.initial_bot_messages_options
        )
        chnew.messages = copy.copy(self.messages)
        return chnew

    @staticmethod
    def fromJSON(obj_json):
        obj_dict = json.loads(obj_json)

        messages_json = obj_dict.pop('messages') 
        ch = ChatHistory(**obj_dict)
        
        if messages_json and len(messages_json)!=0:
            for m_json in messages_json:
                # m = ChatMessage.fromJSON(m_json)
                m = ChatMessage(**m_json)
                ch.add_message(m)

        return ch

        

class ChatForm(Form):
    text_input = StringField('Input',
                            [validators.Length(min=4, max=300)],
                            render_kw={'class': 'form-control chat-text-input-field'}
                            )
