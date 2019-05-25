# django-celery-image-parroter
Code to go with StackAbuse article on using Django with Celery and Redis

### local dev setup

1) install Redis as described in blog post 

2) clone repo

```
git clone https://github.com/amcquistan/image_parroter.git
cd image_parroter
```

3) make virtual env and activate it

```
python3 -m venv venv
source venv/bin/activate
```

4) install python requirements

```
pip install -r requirements.txt
```

5) start redis-server in its own terminal window

```
redis-server
```

6) start celery worker in its own terminal window with the python virtual env from step 3 activated and in the same directory as the manage.py script

```
(venv) celery worker -A image_parroter --loglevel=info
```

7) start django dev server, again in its own terminal window with the python virtual env from step 3 activated and in the same directory as the manage.py script

```
(venv) python manage.py runserver
```

Once these are complete you should be able to point your browser to http://localhost:8000 and see the Thumbnailer application
