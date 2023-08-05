========
Overview
========



Middleware and templatetag for Django to utilize HTTP/2 push for assets included in a Django template. The
middleware injects a `Link` header in each response if there are files to be pushed to the client. All files in the
template which are suitable for HTTP/2 push should be included with the ``staticpush`` templatetag instead of the
vanilla ``static`` templatetag. The former simply augments the later and registers the resulting static URL with the
middleware.

This package currently supports Apache2 webservers with ``mod_http2`` enabled, as the actual HTTP/2 push is offloaded to the
webserver.

.. warning::

    This is ALPHA code. Do not use in production! It only serves as a proof-of-concept for now.

    Conditional HTTP/2 push is not supported yet. This means that your site will actually perform worse than
    over HTTP/1.1 because each response will trigger a push of all incldued assets, irrespective of any cache on the
    webbrowser.

Installation
============

::

    pip install django-static-push

Documentation
=============

https://django-static-push.readthedocs.io/en/latest/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox


Changelog
=========

0.1.0 (2016-01-29)
-----------------------------------------

* First release on PyPI.


