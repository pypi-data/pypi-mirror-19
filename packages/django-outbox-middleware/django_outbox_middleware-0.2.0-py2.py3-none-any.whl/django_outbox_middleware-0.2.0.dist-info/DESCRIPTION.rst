=============================
Django Outbox Middleware
=============================

.. image:: https://badge.fury.io/py/django-outbox-middleware.svg
    :target: https://badge.fury.io/py/django-outbox-middleware

.. image:: https://travis-ci.org/ArtProcessors/django-outbox-middleware.svg?branch=master
    :target: https://travis-ci.org/ArtProcessors/django-outbox-middleware

.. image:: https://codecov.io/gh/ArtProcessors/django-outbox-middleware/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/ArtProcessors/django-outbox-middleware

Your project description goes here

Documentation
-------------

The full documentation is at https://django-outbox-middleware.readthedocs.io.

Quickstart
----------

Install Django Outbox Middleware::

    pip install django-outbox-middleware

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_outbox_middleware.apps.DjangoOutboxMiddlewareConfig',
        ...
    )

Add Django Outbox Middleware's URL patterns:

.. code-block:: python

    from django_outbox_middleware import urls as django_outbox_middleware_urls


    urlpatterns = [
        ...
        url(r'^', include(django_outbox_middleware_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage




History
-------

0.1.0 (2017-01-31)
++++++++++++++++++

* First release on PyPI.


