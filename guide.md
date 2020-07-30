# Guide
Clone this repo first, and `cd image-editor`.

## Project id

```
summer20-sps-68
```
On cloud shell, type
```
gcloud config set project summer20-sps-68
```
to start shell session bind to project.

## Setting up
### Installing requirements
```
python3 -m pip install -r requirements.txt
python3 -m pip install -r requirements-test.txt
python3 -m pip install -r requirements-dev.txt
```

### Setting `$PATH` variables
> On cloud shell

To enable `python3` package scripts (such as `flask`, `pytest` ...).
```
echo 'PATH=$PATH:/home/<username>/.local/bin' >> ~/.bashrc 
source ~/.bashrc
```
Replace `<username>` with your sps username.

### Local developlment
In the app folder, type
```
# set port to 8080
gunicorn --bind=:8080 app:application --reload
```
You can set port number to whatever you like.
   
Or, simply run
```
./start.sh
```
Modify the port number in the `start.sh` file as you wish.

### Test endpoint
- When using Google Cloud Shell, go to (for example) `https://8080-dot-13002410-dot-devshell.appspot.com/api/v1/hello/world` (Click on the Web preview button you've used when using the portfolio to fire up a webpage). 
- When using your local computer, go to `http://0.0.0.0:8080/api/v1/hello/world`.

and see if there is a `{hello:world}` json string.

## Project Structure
- `app/web`: any frontend (css, js, html files)
- `app/imaging`: any image processing features (backend)
- `__init__.py`: main server file (backend)

```bash
- app
    - web
        - static
            - js
            - css
            -fonts
        - templates # for html files
            - index.html
            - ...
    - imaging
        - feature1/
        - feature2/
        - ...
    - __init__.py # main flask app (server)
    - data/ # cached data from client
```
You can go to the base url and see if there is a red Hello showing.

## References

Some questions we've stumbled across - and its solutions.

## Flask
### Returning data from Flask view
- [Return as json](https://stackoverflow.com/questions/13081532/return-json-response-from-flask-view)
- [Returning images](https://stackoverflow.com/questions/7877282/how-to-send-image-generated-by-pil-to-browser)

### Serving static/template files with `flask`
[Link](https://stackoverflow.com/questions/20646822/how-to-serve-static-files-in-flask).

### Multiple routes for view function
[Link](https://stackoverflow.com/questions/17285826/flask-redirecting-multiple-routes)

### Receving data
[Link](https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request)

## Javascript
### Uploading files using `ajax` and `jQuery`
[Link](https://stackoverflow.com/questions/18334717/how-to-upload-a-file-using-an-ajax-call-in-flask)

Note: to use `jQuery`, you need to add a `script` reference to the web-hosted jQuery library in the html file.
```
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
```

### Placing `<script>`
[This link](https://developer.yahoo.com/performance/rules.html#js_bottom) suggests putting `script` tags at the bottom of the html (just before closing `body`) for performance boost (but still varies case by case).

### `FileReader` as `async`
- [Link 1](https://simon-schraeder.de/posts/filereader-async/)

### Drag-and-Drop
[Link](https://pjchender.blogspot.com/2017/08/html5-drag-and-drop-api.html)

