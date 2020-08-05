from PIL import Image
from PIL.ImageFilter import GaussianBlur
import numpy as np
from scipy.signal import convolve2d

def spatial_kernel(s=1, reduce=True):
    l = int(s * 2) | 1  # determine kernel size
    x = np.tile((np.arange(l) - l // 2).reshape(1, l), (l, 1))
    y = np.transpose(x)
    d = x**2 + y**2
    g = np.exp(-d / (2 * (s**2))) / (2 * np.pi * (s**2))
    if reduce:
        g /= np.sum(g.ravel())
    return g

def range_kernel(I, s=1, reduce=True):
    assert I.shape[0] == I.shape[1]
    l = I.shape[0]
    I = I.copy().astype(np.float64)
    I = np.abs((I - I[l // 2, l // 2]))  # minus center pixel value
    k = np.exp(-I / (2 * (s**2))) / (2 * np.pi * (s**2))
    if reduce:
        k /= np.sum(k.ravel())
    return k

def bilateral_filter(img, s1, s2):
    img = np.array(img.convert('L'))  # convert to grayscale
    
    g = spatial_kernel(s = s1, reduce = False)
    L = g.shape[0]

    h, w = img.shape

    padded_img = np.pad(img, pad_width = L // 2, mode = "edge").astype(np.float64)
    filtered = np.zeros(img.shape, dtype=np.float64)
    for i in range(L // 2, h + L // 2):
        for j in range(L // 2, w + L // 2):
            I = padded_img[i - L // 2: i + L // 2 + 1, j - L // 2: j + L // 2 + 1]
            k = range_kernel(I, s = s2, reduce = False)
            W = np.multiply(g, k).ravel()
            p = np.dot(I.ravel(), W) / np.sum(W)
            filtered[i - L // 2, j - L // 2] = p
    filtered = filtered.astype(np.uint8)
    return Image.fromarray(filtered)