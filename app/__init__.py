"""
Primary Flask app

"""
import os
from flask import Flask, render_template, request
from flask_cors import CORS

from .api import api as api_blueprint
from .errors import add_error_handlers

def create_app():
    app = Flask(__name__, static_url_path='', 
        static_folder='web/static', template_folder='web/templates'
    )
    CORS(app, resources={r'/*': {'origins': '*'}})
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    add_error_handlers(app)
    return app

application = create_app()

@application.route("/")
def hello():
    return render_template('index.html')

@application.route("/upload", methods=["GET", "POST"])
def recieve_file():
    uploaded_file = request.files.get('file')
    uploaded_file.save(os.path.join('data', uploaded_file.filename))
    return render_template('index.html')