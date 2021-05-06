## CHAT API
# Virtual Env

````bash
$ python3.7 -m venv env

$ source env/bin/activate
````
# Generate Secret Key

````bash
$ base64 /dev/urandom | head -c50
````

# Install reqs

````
pip install -r requirements.txt 

pip freeze > requirements.txt

python manage.py makemigrations

python manage.py migrate
````

https://docs.djangoproject.com/en/3.0/topics/migrations/

# OpenAPI DOC

http://BASE_URL/openapi?format=openapi-json


# static files

see https://docs.djangoproject.com/en/3.0/howto/static-files/deployment

````
$ python manage.py  collectstatic
````

# locale

django-admin makemessages -l es
django-admin compilemessages

# dev server

python manage.py runserver

# kill debug process

sudo lsof -t -i tcp:8000 | xargs kill -9

