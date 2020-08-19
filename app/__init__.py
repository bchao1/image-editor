"""
Primary Flask app

"""
import os
from flask import Flask, render_template, request
from flask_cors import CORS

from PIL import Image 

from .api import api as api_blueprint
from .errors import add_error_handlers
from .utils import serve_pil_image, b64ToImage

from .imaging.filters import filter_dict
from .imaging.enhance import enhance_dict
from .imaging.quantize import quantize_dict

import json 

def create_app():
    app = Flask(__name__, static_url_path='', 
        static_folder='web/static', template_folder='web/templates'
    )
    CORS(app, resources={r'/*': {'origins': '*'}})
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    add_error_handlers(app)
    return app

application = create_app()
application.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
application.cache = {}  # mimick datastore

@application.route("/")
@application.route("/index.html")
def index_page():
    return render_template('index.html')

@application.route("/stitch.html")
def stitch_page():
    return render_template('stitch.html')

@application.route("/uploadmultiple", methods=["GET", "POST"])
def recieve_multiple_files():
    """ Recieve uploaded files from client.

    Returns:
        Response consisting of the processed image file and status code.
    """
    
    uploaded_files = request.files.getlist('file')  # get list of files uploaded

    file_ordering = request.values.get('order').split(',')
    file_ordering = [int(x) for x in file_ordering]

    files = [uploaded_files[i] for i in file_ordering]

    img_file = files[0]
    file_extention = img_file.filename.split('.')[-1]  # get file extension
    print('File received', img_file.filename)
    print('File extension', file_extention)
    
    with Image.open(img_file.stream) as img:
        # process PIL image (plugin processing functions here)
        img = to_gray(img)
        
        return serve_pil_image(img, file_extention), 200

@application.route("/shareimage", methods=["GET", "POST"])
def recieve_share_image():
    # Save (key, value) = (img id, img data) pair to binary store
    b64str = request.values.get('image_data').split("base64,")[-1]
    img_id = request.values.get('image_id')
    print("Recieved image ", img_id)
    img = b64ToImage(b64str)  # return PIL image
    return "Share Success!", 200

@application.route("/undo-op", methods=["POST"])
def undo_operation():
    sessID = request.values.get("sess")
    return "Undo op", 200

@application.route("/redo-op", methods=["POST"])
def redo_operation():
    sessID = request.values.get("sess")
    return "Redo op", 200

@application.route("/uploadsingle", methods=["GET", "POST"])
def recieve_single_file():
    """ Recieve single uploaded file from client

    Returns:
        Response consisting of the processed image file and status code.
    """
    
    print(request.files)
    uploaded_file = request.files.get('file')
    image_op = request.values.get('op')
    op_magnitude = request.values.get('mag')
    sess_id = request.values.get('sess')
    print(image_op, op_magnitude, sess_id)
    if sess_id not in application.cache:
        application.cache[sess_id] = []  # create cache sequence
    if op_magnitude:
        op_magnitude = float(op_magnitude)
    file_extention = uploaded_file.filename.split('.')[-1]  # get file extension
    print('File received', uploaded_file.filename)
    print('File extension', file_extention)
    img_data = request.get

    with Image.open(uploaded_file.stream) as img:
        # process PIL image (plugin processing functions here)
        if len(application.cache[sess_id]) == 0:  # original image
            application.cache[sess_id].append(img)
        if "filter" in image_op:                
            f = filter_dict[image_op]
            if "bilateral" in image_op:
                img = f(img, 3, 5)
            else:
                img = f(img)
        elif "enhance" in image_op:
            f = enhance_dict[image_op]
            img = f(img, op_magnitude)
        elif "quantize" in image_op:
            f = quantize_dict[image_op]
            img = f(img, int(op_magnitude))
        application.cache[sess_id].append(img)  # store image to cache
        print(application.cache)
        return serve_pil_image(img, file_extention), 200