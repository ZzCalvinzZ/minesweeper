# Django Minesweeper #
A Minesweeper app for playing minesweeper. written in Python with Django

## Installation
* Clone this repository wherever you like 
* Install python and pip if you haven't already
* Install MySQL and configure with database name minesweeper and username and password as calvin or whatever you put in your local.py
* Add a local.py in minesweeper/settings with the following (don't forget to change the secret key):

```
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'minesweeper',                      # Or path to database file if using sqlite3.
        # # The following settings are not used with sqlite3:
        'USER': 'calvin',
        'PASSWORD': 'calvin',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

SECRET_KEY = 'whateversecretkeyyouwant'
```

* install from requirements.txt:
```
pip install -r requirements.txt
```

* sync database with:

```
./manage.py syncdb
```

* now run the server (runs on port 8000):

```
./manage.py runserver
```
