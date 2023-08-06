=============================
Django Elasticsearch Flex
=============================

.. image:: https://badge.fury.io/py/dj-elasticsearch-flex.png
    :target: https://badge.fury.io/py/dj-elasticsearch-flex

.. image:: https://travis-ci.org/prashnts/dj-elasticsearch-flex.png?branch=master
    :target: https://travis-ci.org/prashnts/dj-elasticsearch-flex

Elasticsearch for Django which lets you do stuff.

Documentation
-------------

The full documentation is at https://dj-elasticsearch-flex.readthedocs.io.

Quickstart
----------

Install Django Elasticsearch Flex::

    pip install dj-elasticsearch-flex

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'elasticsearch_flex.apps.ElasticsearchFlexConfig',
        ...
    )

Add Django Elasticsearch Flex's URL patterns:

.. code-block:: python

    from elasticsearch_flex import urls as elasticsearch_flex_urls


    urlpatterns = [
        ...
        url(r'^', include(elasticsearch_flex_urls)),
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
