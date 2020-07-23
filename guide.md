# Guide
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

### Test endpoint
- When using Google Cloud Shell, go to (for example) `https://8080-dot-13002410-dot-devshell.appspot.com/api/v1/hello/world`. 
- When using your local computer, go to `http://127.0.0.1:8080/api/v1/hello/world`.

and see if there is a `{hello:world}` json string.

