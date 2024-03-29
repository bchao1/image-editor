# Cool Image Editor
> Google SPS '20 Project Page

More than just filters 😎.

## Guidelines
Please refer to [this Document](./guide.md). For template usage, refer to [this document](./template.md).

## Features
> Current deployed app is here: https://summer20-sps-68.df.r.appspot.com. Source code is in dev branch `brian_dev`.

- Frontend
    - Upload images 
    - Select image operations
    - Display uploaded/processed preview images
    - Slide bar for operation magnitudes
    - Multiple image upload
    - Multiple image drag and drop reordering
    - Download images
- Backend
    - Flask app skeleton 
- Image processing functions
    - `imaging/filters`
        - sobel filter
        - binarize image color
        - canny edge detector
        - gray scale
        - otsu's method
    - `imaging/enhance`
        - color
        - brightness
        - contrast
        - saturation
        - noise 
        - 'warm', 'vintage' and some other filters
    - `imaging/quantize`:
        - median-cut quantization
        - kmeans quantization
