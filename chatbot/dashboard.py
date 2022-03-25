"""
Dashboard view.
"""
from flask import Blueprint, render_template

from chatbot.auth import login_required
from chatbot.utils import get_activity_plot, get_error_distribution_plot

# Create a blueprint for authentication
bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/', methods=('GET',))
@login_required
def dashboard():
    """ Route for the user dashboard
    """

    fig_activity_html = get_activity_plot()
        
    return render_template('dashboard/dashboard.html', plot=fig_activity_html)



@bp.route('/statistics', methods=('GET',))
@login_required
def statistics():
    """ Route for the user learning center
    """

    fig_activity_html = get_activity_plot()

    fig_grammar_html = get_error_distribution_plot()
        
    return render_template('dashboard/statistics.html', 
                            plot_activity=fig_activity_html,
                            plot_grammar=fig_grammar_html,
                            )

