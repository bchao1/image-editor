from PIL import ImageEnhance


def adjust_brightness(img, m=2):
    return ImageEnhance.Brightness(img).enhance(m)

def adjust_contrast(img, m=2):
    return ImageEnhance.Contrast(img).enhance(m)

def adjust_sharpness(img, m=2):
    return ImageEnhance.Sharpness(img).enhance(m)

def adjust_color(img, m=2):
    return ImageEnhance.Color(img).enhance(m)

enhance_dict = {
    "enhance-brightness": adjust_brightness,
    "enhance-contrast": adjust_contrast,
    "enhance-sharpness": adjust_sharpness,
    "enhance-color": adjust_color
}