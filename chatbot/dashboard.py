"""
Dashboard view.
"""
from flask import Blueprint, render_template, request, session, current_app
from wtforms import Form, StringField, validators
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
from plotly.io import to_html

from chatbot.auth import login_required

# Create a blueprint for authentication
bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/', methods=('GET',))
@login_required
def dashboard():
    """ Route for the user dashboard
    """

    fig_html = get_plot()
    
        
    return render_template('dashboard/dashboard.html', plot=fig_html)


def get_plot():
    from datetime import datetime, timedelta

    def get_daily_chat_data():
        today = datetime.today()
        date_range = pd.date_range(today-timedelta(days=14), today)
        chats = [0,1,5,4,0,3,2,3,0,2,0,1,3,2,4]
        data = pd.DataFrame({'date': date_range, 'chats': chats})
        return data


    # data_canada = px.data.gapminder().query("country == 'Canada'")
    data = get_daily_chat_data()
    fig = px.bar(data, x='date', y='chats', height=300,
                labels={'chats': 'chats', 'date': ''}
                )
    fig.data[0].marker.color = '#17C3B2'
    # fig = fig.update_layout(displayModeBar= False)
    fig.update_traces(
        hoverinfo='none',
        hovertemplate=None
    )
    # fig.update_xaxes({'visible': False})

    fig_html = to_html(fig, full_html=False, include_plotlyjs=False, config={"displayModeBar": False})
    return fig_html