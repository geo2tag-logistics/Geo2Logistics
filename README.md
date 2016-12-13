This project is built on Python-Django stack.

Task
----

https://geo2tag.atlassian.net/wiki/pages/viewpage.action?pageId=45514805

Getting Started
---------------

You need to download and install Python 3.5.x, PyCharm 2016 professional

Then install django

```
pip install django
```


Deployment
----------
Install required libraries.
```
pip install -r /path/to/requirements.txt
```

After cloning you should be able to run this as a django application. You can
run it via your IDE or from the command line.

Run manage.py to manage application. The tool can be fetched from Tools -> Run manage.py Task

1. Make migrations if models were changed

```
makemigrations
```

2. Migrate database if needed

```
migrate
```

3. Start server

```
runserver
```

To create admin and get access to admin tool you should type

```
createsuperuser
```
Default admin username/password pair created is: admin/adminadmin

Initial Endpoints
-----------------

You should be able to visit the following endpoints on your new running
instance..

Login page.

    http://127.0.0.1:8000/

Django Admin tool.

    http://127.0.0.1:8000/admin/

References
----------

Helpful links

[https://habrahabr.ru/post/240463/](https://habrahabr.ru/post/240463/) <BR>
[http://jsman.ru/mongo-book/](http://jsman.ru/mongo-book/) <BR>
[https://docs.djangoproject.com/en/1.10/](https://docs.djangoproject.com/en/1.10/) <BR>
[https://www.youtube.com/watch?v=IZqBTPmxoew](https://www.youtube.com/watch?v=IZqBTPmxoew) <BR>
[http://geo2tag.org/?tag=geo2tag_seminars&lang=ru_RU](http://geo2tag.org/?tag=geo2tag_seminars&lang=ru_RU)
