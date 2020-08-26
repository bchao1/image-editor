"""
Primary Flask app

"""
import os
from flask import Flask, render_template, request
from flask_cors import CORS

from PIL import Image 
from google.cloud import storage, datastore

from .api import api as api_blueprint
from .errors import add_error_handlers
from .utils import serve_pil_image, b64ToImage

from .imaging.filters import filter_dict
from .imaging.enhance import enhance_dict
from .imaging.quantize import quantize_dict

import json

BUCKET_NAME = r'staging.summer20-sps-68.appspot.com'
PROJECT_ID = r'summer20-sps-68'

def upload(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

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

@application.route("/share.html")
def stitch_page():
    return render_template('share.html')

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

    # SAVE THIS IMAGE
    img = b64ToImage(b64str)  # return PIL image
    img_name = f'{img_id}.jpg'
    img.save(img_name, 'jpeg')
    upload(BUCKET_NAME, os.path.join(os.getcwd(), img_name), f'Images/{img_name}')
    os.remove(img_name)

    return "Share Success!", 200

@application.route("/undo-op", methods=["POST"])
def undo_operation():
    sessID = request.values.get("sess")
    return "Undo op", 200

@application.route("/redo-op", methods=["POST"])
def redo_operation():
    sessID = request.values.get("sess")
    return "Redo op", 200

@application.route("/like_image", methods=["POST"])
def like_image():
    image_id = request.values.get("image_id")
    likes = request.values.get("likes")
    print("Liked image", image_id, likes)
    
    client = datastore.Client(PROJECT_ID)
    key = client.key('Likes', 'likes_data')
    likes_data = client.get(key)
    likes_data[image_id] = likes
    client.put(likes_data)

    return "Liked image updated", 200

@application.route("/fetch_all_images", methods=["GET"])
def fetch_all_images():
    """
        Return an object of structure:
        {
            'img': {
                image_id: image base 64 data
            },
            'ext: {
                image_id: image file extension
            }
        }
    """    
    print("Fetch images")

    storage_client = storage.Client()
    images = storage_client.list_blobs(BUCKET_NAME, prefix='Images/')

    datastore_client = datastore.Client(PROJECT_ID)
    key = datastore_client.key('Likes', 'likes_data')
    likes_data = datastore_client.get(key)

    ret = dict()
    ret['img'] = dict()
    ret['ext'] = dict()
    ret['likes'] = dict()

    for image in images:
        if image.name[-3:] == 'jpg':
            image.download_to_filename(os.path.join(os.getcwd(), image.name))
            print(os.path.join(os.getcwd(), image.name))
            img = Image.open(image.name)
            width, height = img.size
            if max(width, height) > 800:
                factor = max(width, height)/800
                img.resize((int(width/factor), int(height/factor)))
            b64_str = serve_pil_image(img, 'jpeg').decode()
            ret['img'][image.name] = b64_str
            ret['ext'][image.name] = 'jpg'
            if image.name in likes_data:
                ret['likes'][image.name] = likes_data[image.name]
            else:
                ret['likes'][image.name] = 0
            print(image.name, ret['likes'][image.name])

    return ret, 200

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

# Disable cache
@application.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r