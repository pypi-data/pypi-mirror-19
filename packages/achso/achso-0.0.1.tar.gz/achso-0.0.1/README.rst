=====
AchSo
=====

This is the backend implementation of AchSo: AtCoder Helper Suite.
This software offers several functionalities to manipulate `AtCoder <https://atcoder.jp/>`_ from command-line, and particularly meant to be used through editor/IDE frontends.
Currently we have frontend implementations for the following editors.

* `GNU Emacs <https://github.com/kissge/achso-emacs>`_

Supported Python versions are Python 2.7+ and Python 3.4+, but probably AchSo works well with older versions, which I haven't tested.

Installation
------------

The easiest way to install the package is via ``pip``::

    $ pip install achso

Developing AchSo
----------------

If you want to develop AchSo, a typical workflow should be something like:

* Clone this repository.
* Set up ``virtualenv`` if you want.
* Run ``pip install -e .``.
* Write your code.

Copyright and License
---------------------

This software is licensed under the MIT License (X11 License).

Copyright (C) 2016 Yuto Kisuge
