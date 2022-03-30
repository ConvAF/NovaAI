"""
Dashboard view.
"""
from flask import Blueprint, render_template, current_app

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


    featured_prompts = {key: current_app.prompts[key] for key in
                        ['general_chat_intermediate', 'scenario_restaurant', 'persona_shakespeare']
                        }
        
    return render_template('dashboard/dashboard.html',
                            plot=fig_activity_html,
                            featured_prompts=featured_prompts
                            )



@bp.route('/statistics', methods=('GET',))
@login_required
def statistics():
    """ Route for the user learning center
    """

    fig_activity_html = get_activity_plot()

    fig_grammar_html = get_error_distribution_plot()

    # suggested_prompts = 
    suggested_prompts = {key: current_app.prompts[key] for key in
                        ['general_chat_intermediate', 'scenario_bakery', 'scenario_restaurant']
                        }
        
    return render_template('dashboard/statistics.html', 
                            plot_activity=fig_activity_html,
                            plot_grammar=fig_grammar_html,
                            suggested_prompts=suggested_prompts
                            )

