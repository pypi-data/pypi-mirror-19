========
Flask-FS
========














Simple and easy file storages for Flask


Compatibility
=============

Flask-FS requires Python 2.7+ and Flask 0.10+.

Amazon S3 support requires Boto3.

GridFS support requires PyMongo 3+.

OpenStack Swift support requires python-swift-client.


Installation
============

You can install Flask-FS with pip:

::

    $ pip install flask-fs
    # or
    $ pip install flask-fs[s3]  # For Amazon S3 backend support
    $ pip install flask-fs[swift]  # For OpenStack swift backend support
    $ pip install flask-fs[gridfs]  # For GridFS backend support
    $ pip install flask-fs[all]  # To include all dependencies for all backends


Quick start
===========

::

    from flask import Flask
    import flask_fs as fs

    app = Flask(__name__)
    fs.init_app(app)

    images = fs.Storage('images')


    if __name__ == '__main__':
        app.run(debug=True)


Documentation
=============

The full documentation is hosted `on Read the Docs <http://flask-fs.readthedocs.org/en/latest/>`_

Changelog
=========

0.2.1 (2017-01-17)
------------------

- Expose Python 3 compatibility

0.2.0 (2016-10-11)
------------------

- Proper github publication
- Initial S3, GridFS and Swift backend implementations
- Python 3 fixes


0.1 (2015-04-07)
----------------

- Initial release



