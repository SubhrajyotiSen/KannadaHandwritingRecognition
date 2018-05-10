#!/bin/sh

python3.5 manage.py makemigrations hwrapp
python3.5 manage.py migrate
python3.5 manage.py runserver
