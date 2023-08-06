.. image:: https://raw.githubusercontent.com/mindey/subfiles/master/misc/subfiles.png
    :alt: Subfiles Illustration
    :width: 100%
    :align: center

subfiles-cli
============

*A command line program to generate .subfiles*

Purpose
-------

Extracts file subtypes to create or append all found subtypes in a project
to a single file, e.g., .subfiles

Usage
-----

Set up::

    $ pip install subfiles

In any project, or directory, run::

    $ subfiles init > .subfiles

This will output ``.subfiles`` with all different file sub-extensions* in the project.

* sub-extension: a file extension with a second dot, e.g. sub-extension of file:
``hello.new.txt`` is ``.new.txt``.

Development reminder
====================

To publish new version on PyPI::

    $ python setup.py sdist bdist_wheel
    $ twine upload dist/*


