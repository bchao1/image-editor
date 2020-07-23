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

