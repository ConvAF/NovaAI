"""
Chat views.
"""
from flask import (Blueprint, flash, g, render_template, request, session, url_for)

from chatbot.db import get_db
from chatbot.auth import login_required

# Create a blueprint for authentication
bp = Blueprint('chat', __name__, url_prefix='/chat')

# @login_required
@bp.route('/general', methods=('GET', 'POST'))
def general():
    """ Route for general simple chat.
    """

    return render_template('chat/general_chat.html')