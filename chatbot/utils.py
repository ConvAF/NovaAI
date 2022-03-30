import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from plotly.io import to_html
from flask.json import JSONEncoder, JSONDecoder
import flask.json
import json 
from chatbot.chat import ChatHistory


def get_activity_plot():
    """ Returns a plot of the users activity over time
    """

    def get_daily_chat_data():
        today = datetime.today()
        date_range = pd.date_range(today-timedelta(days=14), today)
        chats = [0,1,5,4,0,3,2,3,0,2,0,1,3,2,4]
        data = pd.DataFrame({'date': date_range, 'chats': chats})
        return data

    data = get_daily_chat_data()
    fig = px.bar(data, x='date', y='chats', height=300,
                labels={'chats': 'chats', 'date': ''}
                )
    fig.data[0].marker.color = '#17C3B2'
    fig.update_traces(
        hoverinfo='none',
        hovertemplate=None
    )

    fig_html = to_html(fig, full_html=False, include_plotlyjs=False, config={"displayModeBar": False})
    return fig_html


def get_error_distribution_plot():
    """ Returns a plot of the users grammar error distribution
    """
    error_data = pd.DataFrame({
        'error_labels': ['verbs', 'adjectives', 'adverbs', 'nouns', 'prepositions', 'other'],
        'amount': [30,21,14,8,5,4]
    })
    fig = px.pie(error_data, values='amount', names='error_labels',
            #title='Types of errors',
                color_discrete_sequence=px.colors.sequential.GnBu)

    fig.update_traces(
        hoverinfo='none',
        hovertemplate=None
    )

    fig_html = to_html(fig, full_html=False, include_plotlyjs=False, config={"displayModeBar": False})
    return fig_html


class CustomJSONEncoder(JSONEncoder):
    """ Custom JSON encoder to encode custom objects 
    
    This is included so that the ChatHistory can be JSON-serialized,
    so that it can be saved in the flask session object (which only
    accepts jsons)
    """
    def default(self, obj):
        # return super(CustomJSONEncoder, self).defaults(obj)

        if isinstance(obj, ChatHistory):
            return obj.toJSON()
        return super(CustomJSONEncoder, self).defaults(obj)

        # return JSONEncoder.default(self, obj) # default, if not Delivery object. Caller's problem if this is not serialziable.

class CustomJSONDecoder(JSONDecoder):
    """ Custom JSON decoder to decode custom objects
    see https://github.com/pallets/flask/issues/1351
    """
    def __init__(self, *args, **kwargs):
        # JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
        # super(CustomJSONDecoder, self).__init__(object_hook=self.object_hook, *args, **kwargs)
        super(CustomJSONDecoder, self).__init__(object_hook=self.object_hook)


    def object_hook(self, obj_json):
        # import sys
        # print(obj, file=sys.stdout)
        # return obj
    
        # if '_type' not in obj:
            # return obj
        # Transform chat history to object for processing in Python
        if 'chat_history' in obj_json.keys():
            chat_history_json = obj_json['chat_history']
            obj_json['chat_history'] = ChatHistory.fromJSON(chat_history_json)
        return obj_json

def get_empty_chat_history():
    """ Returns a minimal chat history """
    ch = ChatHistory(prompt_base = "The following is a conversation between a Bot and a User.", tag_bot = "Bot", tag_user = "User")
    return ch

def get_simple_chat_history():
    """ Returns a minimal chat history """
    ch = ChatHistory(prompt_base = "The following is a conversation between a Bot and a User.", tag_bot = "Bot", tag_user = "User")
    ch.add_bot_message("Hello User, how are you doing?")
    ch.add_user_message("Hi Bot! Thank you, I am doing fine. How are you?")
    return ch

def print_chat_history(chat_history: ChatHistory):
    """ Print a chat history to stdout """
    import sys
    print("-----------------\nChat History\n\n", chat_history, file=sys.stdout)
    print(f"-----------------\nChat History\n\n{chat_history.get_as_prompt_with_dialog()}", file=sys.stdout)
        