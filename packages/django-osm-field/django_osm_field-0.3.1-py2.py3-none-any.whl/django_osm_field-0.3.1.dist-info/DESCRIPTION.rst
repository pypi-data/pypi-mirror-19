================
Django OSM Field
================

.. image:: https://img.shields.io/pypi/v/django-osm-field.svg
   :target: https://pypi.python.org/pypi/django-osm-field

.. image:: https://img.shields.io/pypi/l/django-osm-field.svg
   :target: https://pypi.python.org/pypi/django-osm-field

.. image:: https://img.shields.io/pypi/dm/django-osm-field.svg
   :target: https://pypi.python.org/pypi/django-osm-field

.. image:: https://img.shields.io/travis/MarkusH/django-osm-field/master.svg
   :target: https://travis-ci.org/MarkusH/django-osm-field

.. image:: https://img.shields.io/codecov/c/github/MarkusH/django-osm-field/master.svg
   :target: https://codecov.io/github/MarkusH/django-osm-field


Django OpenStreetMap Field

* Free software: MIT license
* Documentation: http://django-osm-field.rtfd.org.

Releasing
=========

* Ensure everything is merged into ``develop``
* Ensure the currently active branch is ``develop``
* Run ``tox`` and ensure all tests pass
* Ensure changelog is up to date
* Change to branch ``master``
* Merge branch ``develop``
* Run ``bumpversion major|minor|patch``
* Push changes and tags to Github
* Build Python packages with ``python setup.py sdist bdist_wheel``
* Upload package with ``twine upload -s dist/[.whl-FILE-TO-UPLOAD] dist/[.tar.gz-FILE-TO-UPLOAD]``.




=======
History
=======

0.3.1 (2017-02-06)
==================

* Properly rendered widgets in formsets
* Added preliminary support for Django 1.11

0.3.0 (2016-07-23)
==================

* Added support for Django 1.8, 1.9, 1.10
* Dropped support for Django 1.4, 1.5, 1.6
* Switched from MapQuest to CartoDB (#15)
* Fixed bug in formsets (#7)
* Added ``location_data`` field

0.2.0 (2014-11-10)
==================

* Added support for Django 1.7 migrations (#2)
* Updated styling (#1)
* Forced map refresh on show
* Added tests
* Changed license from BSD to MIT
* Added support for non-default named form fields (those not ending with
  ``_lat`` and ``_lon`` respectively).
* Added documentation


0.1.4 (2014-06-02)
==================

* Add minified JavaScript and CSS sources


0.1.3 (2014-05-28)
==================

* jQuery is not automatically added by the widgets media class anymore


0.1.0 (2014-05-20)
==================

* First release on PyPI.


