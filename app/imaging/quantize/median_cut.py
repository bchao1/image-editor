import numpy as np 
from PIL import Image

def median_cut(img, d):
    d = int(np.log2(d))  # number of colors to levels conversion
    img = np.array(img.convert('RGB')).astype(np.int)
    h, w, _ = img.shape
    img = img.reshape(-1, img.shape[-1])  # flatten color channels (h * w, 3)

    def cut(img, bin_, d):
        if d == 0:
            return [bin_]
        
        new_bin = []
        color_range = np.ptp(img[bin_], axis=0)  # color range of range of pixels
        sort_color_idx = np.argmax(color_range)
        sort_color_channel = img[:, sort_color_idx]
    
        bin_pixels = sort_color_channel[bin_]
        
        permute_idx = np.argsort(bin_pixels)
        b1_idx, b2_idx = np.array_split(permute_idx, 2)

        bin1 = bin_[b1_idx]
        bin2 = bin_[b2_idx]

        return cut(img, bin1, d - 1) + cut(img, bin2, d - 1)

    pixel_indices = np.arange(img.shape[0])
    bins = cut(img, pixel_indices, d)

    for b_idx in bins:
        b = img[b_idx, :]
        c = np.mean(b, axis=0).astype(np.uint8)  # color centroid
        img[b_idx, :] = c
    
    img = img.reshape(h, w, -1).astype(np.uint8)

    return Image.fromarray(img)