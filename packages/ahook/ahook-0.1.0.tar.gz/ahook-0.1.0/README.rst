ahook
===============================

.. image:: https://travis-ci.org/akun/ahook.svg?branch=master
   :target: https://travis-ci.org/akun/ahook
   :alt: Build Status

.. image:: https://landscape.io/github/akun/ahook/master/landscape.svg?style=flat&badge_auth_token=3c37a8bc4b674b41a9c25c18fc9a21d1
   :target: https://landscape.io/github/akun/ahook/master
   :alt: Code Health

.. image:: https://coveralls.io/repos/github/akun/ahook/badge.svg?branch=master
   :target: https://coveralls.io/github/akun/ahook?branch=master
   :alt: Coverage Status

a collection of Git hooks

* Free software: MIT license
* Documentation: http://ahook.rtfd.io/

Features
--------

* commit-msg

  + validate commit message

* pre-push

  + validate branch name

Install
-------

::

   pip install ahook

   # Git 2.9+
   # git config core.hooksPath hooks
   ln -s /usr/local/bin/commit-msg .git/hooks/commit-msg
   ln -s /usr/local/bin/pre-push .git/hooks/pre-push

Examples
--------

TODO

Changelog
---------

0.1.0
~~~~~~~~~~~~~~~~~~~~~~~~~~

2016-12-23

* init project
* commit-msg: validate commit message
* pre-push: validate branch name

Contributing
------------

::

   git clone git@github.com:akun/ahook.git
   cd ahook
   virtualenv .
   make

Credits
-------

* akun <6awkun@gmail.com>

Add your name and email, detail in: https://github.com/akun/ahook/graphs/contributors
