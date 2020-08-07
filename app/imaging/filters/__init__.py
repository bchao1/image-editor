from PIL import Image
import numpy as np 
from scipy import ndimage
from skimage import feature, filters
import collections
from .bilateral import bilateral_filter


def to_gray(img):
    gray_img = img.convert('L')
    return gray_img

def sobel_filter(img):
    gray_img = to_gray(img)  # convert to grayscale
    np_img = np.asarray(gray_img)  # convert to numpy array 
    edge_img = filters.sobel(np_img)  # perform sobel filter
    return Image.fromarray((edge_img * 255).astype(np.uint8))

def canny_edge_detector(img):
    gray_img = to_gray(img) # convert to grayscale
    np_img = np.asarray(gray_img) / 255  # convert to numpy array and rescale to 0~1
    edge_img = feature.canny(np_img).astype(np.int) * 255 # perform canny edge detection
    return Image.fromarray(edge_img.astype(np.uint8))

def two_color(img):
    fmask = np.asarray(binarize_otsu(img)).astype(np.int)
    bmask = 1 - fmask

    c1 = np.dstack([np.full_like(fmask, np.random.random()*255) for _ in range(3)]).astype(np.uint8)
    c2 = 255 - c1
    fmask = np.dstack([fmask] * 3)
    bmask = np.dstack([bmask] * 3)

    img = c1 * fmask + c2 * bmask
    return Image.fromarray(img.astype(np.uint8))

def binarize_median(img):
    gray_img = to_gray(img)
    I = np.array(gray_img).ravel()
    thresh = np.median(I)
    fn = lambda pixel: 255 if pixel > thresh else 0
    bin_img = gray_img.point(fn, mode='1')
    return bin_img 

def binarize_otsu(img):
    I = np.array(to_gray(img))  # convert to grayscale
    
    pixels, counts = np.unique(I.ravel(), return_counts = True)  # count pixel value occurences

    hist = np.zeros(256)
    hist[pixels] = counts  # color histogram

    total_pixels = I.size  # number of pixels in the image
    total_pixels_weighted = np.dot(np.arange(256), hist)  # sum of pixel values weighted by their occurence

    w0 = 0  # w1 = total_pixels_weighted - w0
    w0_sum = 0
    max_sigma = -np.inf
    thresh = 0

    for p, cnt in enumerate(hist):
        w1 = total_pixels - w0
        if w0 > 0 and w1 > 0:
            w1_sum = total_pixels_weighted - w0_sum
            mu0 = w0_sum / w0 
            mu1 = w1_sum / w1
            new_sigma = w0 * w1 * ((mu0 - mu1)**2)
            if new_sigma > max_sigma:
                thresh = p
                max_sigma = new_sigma
        w0 += cnt
        w0_sum += (p * cnt)


    mask_ostu = (I > thresh).astype(np.int)
    B_otsu = (255 * mask_ostu).astype(np.uint8)

    return  Image.fromarray(B_otsu)


filter_dict = {
    'filter-grayscale': to_gray,
    'filter-two-color': two_color,
    'filter-canny': canny_edge_detector,
    'filter-sobel': sobel_filter,
    'filter-black-white-otsu': binarize_otsu,
    'filter-black-white-median': binarize_median,
    'filter-bilateral': bilateral_filter
}