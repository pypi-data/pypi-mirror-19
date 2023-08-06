Cspark-python is a `cisco spark <https://www.ciscospark.com/>`_ library for bots
================================================================================

`|Build| <https://travis-ci.org/Matvey-Kuk/cspark-python>`_
`|Downloads| <https://pypi.python.org/pypi/cspark-python>`_
`|Version| <https://pypi.python.org/pypi/cspark-python>`_

Why?
~~~~

1. Spark API provides only one mechanism to notify bot about updates:
   Webhooks. "Webhooks require that the Cisco Spark Cloud be able to
   reach your backend over HTTP"
   `(link) <https://developer.ciscospark.com/webhooks-explained.html#auth>`_
   It's not comfortable to develop and test bots on public server so
   Cspark-python emulates update mechanism using REST API.
2. Class-based routers and request handlers allow you to use
   Django-style project structure for complex projects.

Howto:
~~~~~~

1. Install with PIP: ``pip install cspark-python``

2. Then go to developer website, `create new
   bot <https://developer.ciscospark.com/apps.html>`_ and achieve
   **Access Token**. Be careful and don't copy your own **Access Token**
   it will cause funny situation.

    If you stacked with icon uploading mechanism (as I always do), you
    can use random photo of a cat:
    https://pbs.twimg.com/profile\_images/562466745340817408/\_nIu8KHX.jpeg

3. Use examples to start your first bot. Don't forget to change **Access
   Token**.

    Currently only 0\_simple\_echo.py example works, others are
    concepts.

P.S. Cisco Spark team use term "SDK" for libraries which use their
API... Ok. That's **Cisco Spark Python SDK**.

.. |Build| image:: https://travis-ci.org/Matvey-Kuk/cspark-python.svg?branch=master
.. |Downloads| image:: https://img.shields.io/pypi/dm/cspark-python.svg
.. |Version| image:: https://img.shields.io/pypi/v/cspark-python.svg
