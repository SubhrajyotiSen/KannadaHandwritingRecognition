#!/bin/sh

python3.6 manage.py makemigrations hwrapp
python3.6 manage.py migrate
python3.6 manage.py runserver 0:8000
