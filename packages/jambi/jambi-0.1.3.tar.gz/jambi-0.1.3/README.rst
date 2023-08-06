.. image:: https://i.imgur.com/vf8CyKL.png

jambi
=====

a peewee database migration manager (in development)

About
-----
The `peewee ORM <https://github.com/coleifer/peewee>`_ has limited migration support through its extension, playhouse. A ``SchemaMigrator`` is supplied that can run schema-altering statements, but there is no concept of versioning the database. By giving your database a version number, jambi can help you keep your database schema revisions organized, and allows you to incrementally upgrade if desired.

Getting Started
---------------
- install with pip
    ``pip install jambi``
- create a jambi config file in your favorite directory
    ``cd myproj/db && touch jambi.conf``
- see the section entitled 'Configuration' to learn about what must be in jambi.conf
- run jambi!
    ``jambi --help``

Supported Operations
--------------------
    **init** -- create the jambi table and set the version to 0

    **inspect** -- return the database's current version

    **latest** -- retuns the latest migration version

    **upgrade <version>** -- upgrade your database to the supplied version

    **makemigration** -- generate a new migration version from template

Configuration
-------------
Jambi needs to know how to connect to your database, and where your migrations are stored, which can be conveyed though the jambi.conf configuration file. **Currently jambi only supports PostgreSQL**, but support for others wouldn't be hard to implement -- feel free to make a pull request!) Jambi will look for your configuration file in your current working directory.

Here is an example jambi.conf, set up to connect to a vanilla postgres database:

.. code-block:: ini

    [database]
    database=test
    schema=public
    host=localhost
    user=postgres
    password=

    [migrate]
    location=./migrations/


Contributing
------------
Pull requests are welcome, and please open issues for any bugs, enhancements, or feature requests.

Disclaimer
----------
I claim no responsibility for bugs or other misuse of this tool resulting in loss of data or any other unintended side-effect. This is still an alpha release, so don't expect too much. (see: Contributing).
