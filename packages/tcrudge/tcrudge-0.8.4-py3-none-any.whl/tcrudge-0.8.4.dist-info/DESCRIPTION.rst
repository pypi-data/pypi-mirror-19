TCrudge - simple async CRUDL based on Tornado and Peewee ORM (Peewee
Async)

|Documentation Status| |Build Status| |Code Climate| |Issue Count|
|Coverage Status|

Full documentation (http://tcrudge.readthedocs.io/en/latest/)

What is it?
===========

Simple configurable framework to create CRUDL (Create, Read, Update,
Delete, List) for models

Why?
====

Tornado is fast. Peewee is great. REST is wonderful.

Dependencies
============

-  Tornado (https://github.com/tornadoweb/tornado)
-  Peewee (https://github.com/coleifer/peewee)
-  Peewee-async (https://github.com/05bit/peewee-async)
-  Modified JSON schema generator by [Shalamov Maxim]
   (https://github.com/mvshalamov)
   (https://github.com/mvshalamov/GenSON)

Installation
============

tcrudge is not distributed by pip (https://pypi.python.org/pypi). So use
installation via GitHub:

::

    pip install git+https://github.com/CodeTeam/tcrudge.git

How to?
=======

Describe models using Peewee ORM. Subclass ``tcrudge.ApiListHandler``
and ``tcrudge.ApiItemHandler``. Connect handlers with models using
model\_cls handler attribute. Add urls to tornado.Application url
dispatcher.

For detailed example see tests (also, tests are available in Docker
container with py.test).

You can run tests in docker container only. You'll need docker and
docker-compose. 1. Go to project root directory 2. Run docker-compose
up, it builts and runs containers. 3. Go to tcrudge container bash:
docker exec -ti tcrudge\_tcrudge\_1 bash 4. Run:
DATABASE\_URL=postgresql://user:dbpass@pg/test pytest

Features?
=========

1. DELETE request on item is disabled by default. To enable it implement
   \_delete method in your model.
2. Models are fat. \_create, \_update, \_delete methods are supposed to
   provide different logic on CRUD operations
3. Django-style filtering in list request: \*\_\_gt\ *, *\ \_\_gte\ *,
   *\ \_\_lt\ *, *\ \_\_lte\ *, *\ \_\_in\ *, *\ \_\_isnull\ *,
   *\ \_\_like\ *, *\ \_\_ilike\ *, *\ \_\_ne\* are supported. Use
   ``/?model_field__<filter_type>=<filter_condition>`` for complex or
   ``/?model_field=<filter_condition>`` for simple filtering.
4. Django-style order by: use ``/?order_by=<field_1>,<field_2>`` etc
5. Serialization is provided by Peewee:
   playhouse.shortcuts.model\_to\_dict. recurse, exclude and max\_depth
   params are implemented in base class for better experience. If you
   want to serialize recurse foreign keys, do not forget to modify
   get\_queryset method (see Peewee docs for details, use ``.join()``
   and ``.select()``)
6. Validation is provided out-of-the box via jsonschema. Just set input
   schemas for base methods (e.g. post\_schema\_input,
   get\_schema\_input etc). Request query is validated for GET and HEAD.
   Request body is validated for *POST*, *PUT* and *DELETE*.
7. Pagination is activated by default for lists. Use default\_limit and
   mac\_limit for customization. Pagination params are set through
   headers (X-Limit, X-Offset) or query: ``/?limit=100&offset=5``. Total
   amount of items is not returned by default. HEAD request should be
   sent or total param set to 1: ``/?total=1``
8. List handler supports default filtering and ordering. Use
   ``default_filter`` and ``default_order_by`` class properties.

Example
=======

Application
-----------

.. code:: python

    app_handlers = [
        ('^/api/v1/companies/', CompanyListHandler),
        ('^/api/v1/companies/([^/]+)/', CompanyDetailHandler)
    ]

    application = web.Application(app_handlers, debug=settings.DEBUG, template_path=settings.TEMPLATE_PATH)


    #ORM
    application.objects = peewee_async.Manager(db)


    def runserver():
        if settings.DEBUG:
            application.listen(settings.PORT, '0.0.0.0')
        else:
            server = HTTPServer(application)
            server.bind(settings.PORT)
            server.start(0)
        loop = asyncio.get_event_loop()
        loop.run_forever()

Model
-----

    DB table must exist; Fields in table must correspond to model fields

.. code:: python

    class Company(CustomBaseModel):
        company_inn = peewee.TextField()
        active = peewee.BooleanField()
        created_at = peewee.DateTimeField()
        updated_at = peewee.DateTimeField()

        class Meta:
            db_table = "company"

Handlers
--------

.. code:: python

    class CompanyDetailHandler(ApiItemHandler):
        model_cls = Company

        get_schema_input = GET_SCHEMA
        put_schema_input = UPDATE_SCHEMA
        delete_schema_input = DELETE_SCHEMA


    class CompanyListHandler(ApiListHandler):
        model_cls = Company

        post_schema_input = INSERT_SCHEMA
        get_schema_input = GET_SCHEMA

        default_filter = {'active': True}

Сontributors
============

-  [Borisov Sergey] (https://github.com/juntatalor)
-  [Shalamov Maxim] (https://github.com/mvshalamov)
-  [Nikolaev Alexander] (https://github.com/wokli)
-  [Krasavina Alina] (https://github.com/thaelathy)

.. |Documentation Status| image:: https://readthedocs.org/projects/tcrudge/badge/?version=latest
   :target: http://tcrudge.readthedocs.io/en/latest/?badge=latest
.. |Build Status| image:: https://travis-ci.org/CodeTeam/tcrudge.svg?branch=master
   :target: https://travis-ci.org/CodeTeam/tcrudge
.. |Code Climate| image:: https://codeclimate.com/github/CodeTeam/tcrudge/badges/gpa.svg
   :target: https://codeclimate.com/github/CodeTeam/tcrudge
.. |Issue Count| image:: https://codeclimate.com/github/CodeTeam/tcrudge/badges/issue_count.svg
   :target: https://codeclimate.com/github/CodeTeam/tcrudge
.. |Coverage Status| image:: https://coveralls.io/repos/github/CodeTeam/tcrudge/badge.svg?branch=master
   :target: https://coveralls.io/github/CodeTeam/tcrudge?branch=master


