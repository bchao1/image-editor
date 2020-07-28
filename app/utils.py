from io import BytesIO
from flask import send_file
import base64

def serve_pil_image(pil_img, ext):
    """ serve a PIL image file as a flask response
    
    Args: 
        pil_img: PIL img file to serve.
        ext: file extension
    Returns:
        A flask send_file response.
    """
    img_io = BytesIO()
    ext = ext.lower()  # normalize extension
    if ext == 'jpg':
        ext = 'jpeg'
    pil_img.save(img_io, ext, quality = 75) #  default quality
    img_io.seek(0) #  go to head of io file
    return base64.b64encode(img_io.getvalue())


