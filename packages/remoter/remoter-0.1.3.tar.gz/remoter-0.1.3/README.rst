=======
remoter
=======


.. image:: https://img.shields.io/pypi/v/remoter.svg
        :target: https://pypi.python.org/pypi/remoter

.. image:: https://img.shields.io/travis/levchik/remoter.svg
        :target: https://travis-ci.org/levchik/remoter

.. image:: https://readthedocs.org/projects/remoter/badge/?version=latest
        :target: https://remoter.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/levchik/remoter/shield.svg
     :target: https://pyup.io/repos/github/levchik/remoter/
     :alt: Updates


Python 3 compatible remote task runner


* Free software: Apache Software License 2.0
* Documentation: https://remoter.readthedocs.io.

Usage
-----

    $ pip instal remoter
    $ vi remoter.yml
    $ remoter tasks run


Config
------

It consists of two main parts: `servers` and `tasks`.
In the `servers` section you define hosts with the auth credentials for SSH connection.
In the `tasks` section you define sequence of tasks to be performed for each server.

Example of what updating a docker-compose django service might look like:

    servers:
      test1:
        host: "127.0.0.1"
        port: 22
        username: "docker"
        password: "docker"
    tasks:
      test1:
        - "docker-compose stop"
        - "git pull origin master"
        - "docker-compose run --rm python manage.py migrate"
        - "docker-compose up -d"


Roadmap
-------

Future plans and tasks are in kanban-like projects here:

https://github.com/levchik/remoter/projects


Development in docker
---------------------

*Build*

    $ docker build -t remoter:latest .

*Run tests*

    $ docker run --rm -it -v $(pwd):/code remoter:latest make test

*Run cli*

    $ docker run --rm -it -v $(pwd):/code remoter:latest python -m remoter.cli


Credits
-------

Implemenetation of test SSH server was taken from https://github.com/carletes/mock-ssh-server

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
