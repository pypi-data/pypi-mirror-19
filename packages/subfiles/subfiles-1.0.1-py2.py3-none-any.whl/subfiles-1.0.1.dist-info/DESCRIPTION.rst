subtypes-cli
============

*A command line program to generate subtypes.txt*


Purpose
-------

Extracts file subtypes to create or append all found subtypes in a project
to a single file, e.g., subtypes.txt

Usage
-----

Set up::

    $ pip install subfiles

In any project, or directory, run::

    $ subfiles init

This will output .subfiles with all different file sub-extensions* in the project.

* sub-extension: a file extension with a second dot, e.g. sub-extension of file:
`hello.new.txt` is `.new.txt`.


