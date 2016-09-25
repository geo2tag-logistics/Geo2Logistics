This project is built on Python-Django-MongoDB stack.

Task
----

https://geo2tag.atlassian.net/wiki/pages/viewpage.action?pageId=45514805

Getting Started
---------------

You need to download and install Python 3.5.2, PyCharm 2016 professional, MongoDB 3.2.9

Then install django

```
pip install django
```


Deployment
----------
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

[https://habrahabr.ru/post/240463/](https://habrahabr.ru/post/240463/)
[http://jsman.ru/mongo-book/](http://jsman.ru/mongo-book/)
[https://docs.djangoproject.com/en/1.10/](https://docs.djangoproject.com/en/1.10/)
[https://www.youtube.com/watch?v=IZqBTPmxoew](https://www.youtube.com/watch?v=IZqBTPmxoew)
[http://geo2tag.org/?tag=geo2tag_seminars&lang=ru_RU](http://geo2tag.org/?tag=geo2tag_seminars&lang=ru_RU)