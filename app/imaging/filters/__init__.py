from PIL import Image
import numpy as np 
from scipy import ndimage
from skimage import feature


def to_gray(img):
    gray_img = img.convert('L')
    return gray_img

def sobel_filter(img):
    gray_img = to_gray(img)  # convert to grayscale
    np_img = np.asarray(gray_img)  # convert to numpy array 
    edge_img = ndimage.sobel(np_img)  # perform sobel filter
    return Image.fromarray(edge_img.astype(np.uint8))

def canny_edge_detector(img):
    gray_img = to_gray(img) # convert to grayscale
    np_img = np.asarray(gray_img) / 255  # convert to numpy array and rescale to 0~1
    edge_img = feature.canny(np_img).astype(np.int) * 255 # perform canny edge detection
    return Image.fromarray(edge_img.astype(np.uint8))


