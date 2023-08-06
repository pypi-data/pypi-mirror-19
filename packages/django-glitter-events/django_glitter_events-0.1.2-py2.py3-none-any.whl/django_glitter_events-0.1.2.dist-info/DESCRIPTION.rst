==============
Glitter Events
==============

Django glitter events for Django.


Installation
============


Getting the code
----------------

You can get **django-glitter-events** by using **pip**:

.. code-block:: console

    $ pip install django-glitter-events

Prerequisites
-------------

Make sure you add ``'glitter_events'``, ``'taggit'`` and ``'adminsortable'`` to your
``INSTALLED_APPS`` setting:

.. code-block:: python

    INSTALLED_APPS = [
        # ...
        'glitter_events',
        'taggit',
        'adminsortable',
        # ...
    ]

URLconf
-------

Add the Glitter Events URLs to your project’s URLconf as follows:


.. code-block:: python

    url(r'^events/', include('glitter_events.urls', namespace='glitter-events'))



