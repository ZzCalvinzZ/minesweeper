# Django Minesweeper #
A Minesweeper app for playing minesweeper. written in Python with Django

## Installation
* Clone this repository wherever you like 
* Install python and pip if you haven't already
* Install PostgreSQL and configure with database name minesweeper and username and password as calvin (or change database info in settings.py)
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