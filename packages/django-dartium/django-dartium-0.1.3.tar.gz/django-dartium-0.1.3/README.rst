==============
django-dartium
==============

.. _introduction:

**django-dartium** provides for a simple way to detect the Dartium web browser and make
it easy to serve Dart sources instead of compiled JavaScript during development.


Installation
============

.. _installation:

**Python 3** and **Django** are the only requirements:

1. Install **django-dartium** with your favorite python tool, e.g. ``pip install django-dartium``.

2. Add ``django_dartium`` to your ``INSTALLED_APPS`` setting.

3. Add ``django_dartium.middleware.DartiumDetectionMiddleware`` to your ``MIDDLEWARE_CLASSES`` setting.

4. Add two named mappings to ``STATICFILES_DIRS``, one named ``dart/build`` which points to the
   build location of the JavaScript output and the other is ``dart/src`` which points to the ``web``
   directory containing your original Dart source. If you created your Django project by running
   ``django-admin startproject your_project`` and placed your Dart sources in
   ``your_project/your_project/dart`` directory, then you would have the following ``STATICFILES_DIRS``:

   .. code-block:: python

     STATICFILES_DIRS = [
       ('dart/build', 'your_project/dart/build/web'),
       ('dart/src', 'your_project/dart/web'),
     ]


Usage
=====

.. _usage:

Load the ``dartium`` tag library into your Django template, call the ``webcomponents`` tag to load
the necessary polyfills and then add a reference to your Dart code via the ``dart`` tag.

A good setup would be to have the following in your ``base.html``:

.. code-block:: html+django

  {% load dartium %}
  <html>
  ...
  <body>
    {% block content %}
    {% endblock %}

    {% webcomponents 'lite' %}
    {% block script %}
    {% endblock %}
  </body>
  </html>

Then in each of your pages where you want to use Dart some Dart script you can add:

.. code-block:: html+django

  {% load dartium %}
  {% block content %}
    ... page content ...
  {% endblock %}
  {% block script %}
    {% dart "your_script.dart" %}
  {% endblock %}

The end result will be that if you browse to this page with Dartium you will get
served your original Dart source but if you are using any other browser you'll
be served ``your_script.dart.js`` from the ``build/web`` directory.
