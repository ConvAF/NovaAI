import os
import json
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, render_template, session

from . import db, auth, chat, dashboard

from .language_model import LanguageModel
from .grammar_correction import GrammarModel

load_dotenv() # Load env variables

def create_app(test_config=None):
    """ Create the application.
    """
    # create and configure the app instance
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'chatbot.sqlite'),
        LOAD_GRAMMAR_MODEL=True
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Ensure required environment vars exist
    env_vars = ['OPENAI_API_KEY', 'OPENAI_ENGINE']
    for var in env_vars:
        assert os.getenv(var)

    # Initialize the database
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(chat.bp)
    app.register_blueprint(dashboard.bp)

    # Register routes
    @app.route('/')
    def index():
        return render_template('index.html')

    # app.config['LOAD_LANGUAGE_MODEL'] = False

    app.language_model = LanguageModel()
    if app.config['LOAD_GRAMMAR_MODEL']:
        app.grammar_correction = GrammarModel(models = 1, use_gpu=False)

    # Load prompts data
    prompts_path = Path(app.root_path) / 'data'/ 'prompts.json'
    app.prompts = json.loads(open(prompts_path,'r').read())


    from chatbot.utils import CustomJSONDecoder, CustomJSONEncoder
    app.json_encoder = CustomJSONEncoder
    app.json_decoder = CustomJSONDecoder


    return app

