========================
 virtualenvwrapper.basic
========================

virtualenvwrapper.basic is a template for virtualenvwrapper_ to create the base
skeleton of a python application when creating a new project directory.


Installation
============

::

  $ pip install virtualenvwrapper.basic


Usage
=====

::

  $ mkproject -t basic new_project


The previous command will create a directory and will populate it with various
files, namely ``ANNOUNCE``, ``AUTHORS``, ``CHANGES``, ``LICENSE``,
``MANIFEST.in``, ``README``, ``requirements.txt`` and ``setup.py``.

The content of each file is matched to the name of your project and your
:code:`git` configuration.

You can set up another reference skeleton directory by specifying the path to
it in the environment variable :code:``VIRTUALENVWRAPPER_BASIC``.

::

  $ VIRTUALENVWRAPPER_BASIC="/my/own/template" mkproject -t basic new_project


virtualenvwrapper.basic supports variables in the content and the name of
files to be replaced when the project files are generated. The following
variables are automatically replaced:

+------------------------------+----------------------------------------------+
| Variable                     | Description                                  |
+==============================+==============================================+
| $PROJECT_NAME                | Replaced by the project name used with       |
|                              | :code:`virtualenvwrapper`.                   |
+------------------------------+----------------------------------------------+
| $AUTHOR_EMAIL                | Replaced by the email configured in git as   |
|                              | :code:`user.email`.                          |
+------------------------------+----------------------------------------------+
| $AUTHOR_NAME                 | Replaced by the name configured in git as    |
|                              | :code:`user.name`.                           |
+------------------------------+----------------------------------------------+
| $YEAR                        | Replaced by the current year.                |
+------------------------------+----------------------------------------------+
| $MONTH                       | Replaced by the current month.               |
+------------------------------+----------------------------------------------+
| $DAY                         | Replaced by the current day.                 |
+------------------------------+----------------------------------------------+

.. _virtualenvwrapper: https://pypi.python.org/pypi/virtualenvwrapper


