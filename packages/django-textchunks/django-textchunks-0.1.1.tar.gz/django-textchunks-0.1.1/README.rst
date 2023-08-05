Django Text Chunks
==================

Insert blocks of text anywhere in in your template

Installation
=============

Install package using pip

::

    $ pip install django-textchunks

Basic usage
===========

Add the ``textchunks`` application to ``INSTALLED_APPS`` in your settings file (usually ``settings.py``)

::

    INSTALLED_APPS = (
        ...
        'textchunks',
        ...
    )


Sync database with ``./manage.py migrate``. After that, add textchunks using
django admin interface and use them on your templates:

.. code-block:: html

    {% load textchunks %}

    <html>
      <head>
        <title>Test</title>
        {% textchunk "google_analytics" %}
      </head>
      <body>
        <h1>Blah blah blah</h1>
        <div id="sidebar">
            ...
        </div>
        <div id="left">
            {% textchunk "home_page_left" %}
        </div>
        <div id="right">
            {% textchunk "home_page_right" %}
        </div>
      </body>
    </html>

Advanced usage
==============

There are two template tags available: ``textchunk`` and ``textchunk_plain``.
Text displayed with ``textchunk`` is not escaped, any html and javascript is
rendered or executed. ``textchunk_plain`` tag uses ``from django.utils.html.escape``
to escape it's content, so it's safe to render user-entered text.

``textchunk`` tag uses django ``Template`` object to render data and has access
to template context. So, text

::

    <span>{{ request.user.username }}</span>

for user with username as `agentsmith` will be rendered as

::

    <span>agentsmith</span>
