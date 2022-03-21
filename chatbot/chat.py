"""
Chat views.
"""
from flask import Blueprint, render_template, request, session, current_app
from wtforms import Form, StringField, validators

from chatbot.auth import login_required

# Create a blueprint for authentication
bp = Blueprint('chat', __name__, url_prefix='/chat')

@bp.route('/general', methods=('GET', 'POST'))
@login_required
def general():
    """ Route for general simple chat.
    """
    form = ChatForm(request.form)

    # Get chat history
    chat_history = session.get('chat_history')
    # Create if not exists
    if not chat_history:
        chat_history = []

    # On text form submission
    if request.method == 'POST':
        if request.form['submit_button'] == 'Clear chat':
            # Clear chat history
            clear_chat_history()
        elif request.form['submit_button'] == 'Send text' and form.validate():
            # Add text to chat history
            chat_history.append(
                {
                    'sender': 'user',
                    'text': form.text_input.data
                }
            )

            # Clear form
            form.text_input.data = ""
            # Get response from bot
            chat_history = get_bot_response(chat_history)
            # Update chat history
            session['chat_history'] = chat_history
        
    return render_template('chat/general_chat.html', form=form)


def get_bot_response(chat_history):
    """ Get response from the bot """
    # Here we have to get the response from the bot
    # chat_history should be sent to the model class
    # Something like:
    # response = model.predict(chat_history)
    # chat_history_new = chat_history.append(response)
    # Dummy response for now
    # chat_history.append(
    #     {
    #         'sender': 'bot',
    #         'text': 'This is an automated dummy reply.'
    #     }
    # )
    chat_history = current_app.grammar_correction.add_correction_to_chat_history(chat_history)
    chat_history = current_app.language_model.add_response_to_chat_history(chat_history)

    return chat_history

def clear_chat_history():
    """ Clear the chat history """
    if session.get('chat_history'):
        session.pop('chat_history')

class ChatForm(Form):
    text_input = StringField('Input',
                            [validators.Length(min=4, max=300)],
                            render_kw={'class': 'chat_text_input_field'}
                            )
