import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from plotly.io import to_html


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
