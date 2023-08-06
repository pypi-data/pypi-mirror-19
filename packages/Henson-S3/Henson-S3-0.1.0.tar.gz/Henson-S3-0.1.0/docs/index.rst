=============
Henson-S3
=============

Henson-S3 is a library that helps to easily interact with S3 from inside a
`Henson <https://henson.readthedocs.io>`_ application.

Installation
============

Henson-S3 can be installed with::

    $ python -m pip install Henson-S3

.. warning::

    Henson-S3 is not yet available on the Python Package Index.

Configuration
=============

The following configuration settings can be added to the application.

+---------------------------+-------------------------------------------------+
| ``AWS_ACCESS_KEY_ID``     | The Access ID used to identify the account.     |
|                           | Defaults to None.                               |
+---------------------------+-------------------------------------------------+
| ``AWS_SECRET_ACCESS_KEY`` | The Access Secret used to identify the account. |
|                           | Defaults to None.                               |
+---------------------------+-------------------------------------------------+
| ``AWS_BUCKET_NAME``       | The name of the default bucket to use. Defaults |
|                           | to None.                                        |
+---------------------------+-------------------------------------------------+
| ``AWS_REGION_NAME``       | The name of the Region where the bucket is      |
|                           | located. Defaults to None.                      |
+---------------------------+-------------------------------------------------+

Usage
=====

.. code::

    from henson import Application
    from henson_s3 import S3

    app = Application('application-with-s3')
    app.settings['AWS_BUCKET_NAME'] = 'my-henson-bucket'

    S3(app)

API
===

.. autoclass:: henson_s3.S3
   :members:

Contents:

.. toctree::
   :maxdepth: 1

   changes



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
