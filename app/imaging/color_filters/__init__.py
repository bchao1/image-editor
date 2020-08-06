import numpy as np
import random
from PIL import Image, ImageDraw


def warm_filter(img):
    
    img_warm = img
    draw = ImageDraw.Draw(img_warm) 
    width = img_warm.size[0] 
    height = img_warm.size[1] 
    pix = img_warm.load()
    
    for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]
                a -= b // 4 
                b -= c // 4 
                c -= a // 4
                draw.point((i, j), (a, b, c))
                
    return img_warm
    
    
def old_filter(img):
    
    img_old = img
    draw = ImageDraw.Draw(img_old) 
    width = img_old.size[0] 
    height = img_old.size[1] 
    pix = img_old.load()
    
    for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]
                red = a
                green = b
                blue = c
                s = red + green + blue
                
                a = a - s // 6 + blue // 10 
                b = b - s // 5 + red // 9
                c = c - s // 6
                
                s = a + b + c
                if (s > 300):
                    a += 7
                    b += 7
                    c += 7
                else :
                    a += 5
                    b += 5
                    c += 6
                    
                if (a > 100) :
                    a -= a // 10
                    
                draw.point((i, j), (a, b, c))

    return img_old
    
    
def green_filter(img):
    
    img_green = img
    draw = ImageDraw.Draw(img_green) 
    width = img_green.size[0] 
    height = img_green.size[1] 
    pix = img_green.load()
    
    for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]
                a -= b // 3
                b -= b // 8
                c -= a // 6
                
                if (b > 100):
                    b -= b//8
                else:
                    b -= b//11
                    
                if (a + c < 100):
                    a += a // 10
                    c += c // 10
                else:
                    a += a // 18
                    c += c // 22
                    
                draw.point((i, j), (a, b, c))
    
    return img_green
    

color_dict = {
    'fil-warm': warm_filter,
    'fil-old': old_filter,
    'fil-green': green_filter
}

