# snazzy

## Environment Setup

Install virtualenv

```
sudo pip install virtualenv
sudo apt-get install python-virtualenv
```

Navigate to the `snazzy` directory and run

```
virtualenv .
```

This should install pip and setuptools in your directory. When you are 
ready to begin working active the environment with `. bin/activate`.
When you are done with your work, deactiavte the environment with
`deactivate`.

## Install Dependencies

```
sudo apt-get install cups
sudo apt-get install libcups2-dev
```

After activating the environment run

```
pip install Flask
pip install ws4py
pip install picamera
pip install wand
pip install pycups
```

## Run with Flask

In bash set your environment variable with `export FLASK_APP=FlaskServer.py`. Then start the server with `flask run`
