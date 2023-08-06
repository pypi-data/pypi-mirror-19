.. image:: https://raw.githubusercontent.com/mindey/subfiles/master/misc/subfiles.png
    :alt: Subfiles Illustration
    :width: 100%
    :align: center

The idea here is to create namespaces for file extensions for all kind of uses. For example, you might want to use secondary level extensions represent and map files with schemas of data instances that they contain. So, ``.subfiles`` is supposed to just contain any metadata that file extensions carry beyond what the file extension represents. For example, it could be a specific format of the CSV, or anything whatsoever, that helps any other programs or humanst to understand the files in project, such as:

Purpose
-------

Extracts file subtypes of files in a directory, so as to have a list of file extensions appearing in directory.

Usage
-----

Set up::

    $ pip install subfiles

In any project, or directory, run::

    $ subfiles -l

This will output files grouped by different file sub-extensions in the project.

Encoding Schemas
----------------

The command can be used to quickly get a prototype for creation of schemas for files with 2nd level extensions.

.. code::

   [.city.csv] - SHORT DESCRIPTION
   MORE INFORMATION

   [.observation.json] - SHORT DESCRIPTION
   MORE INFORMATION


2nd degree ``.subfiles`` shows what file extensions represent and constituted from instances of what ``subtypes`` (schemas).

.. code::

   [.graph.json] - https://www.wikidata.org/wiki/Q182598
   cat: https://www.wikidata.org/wiki/Q146
   dog: https://www.wikidata.org/wiki/Q144
   love: https://www.wikidata.org/wiki/Q316
   
   [.products.csv] - https://www.wikidata.org/wiki/Q278425
   url: https://www.wikidata.org/wiki/Q42253
   currency: https://www.wikidata.org/wiki/Q8142
   price: https://www.wikidata.org/wiki/Q160151
   name: https://www.wikidata.org/wiki/Q1786779



Development reminder
====================

To publish new version on PyPI::

    $ python setup.py sdist bdist_wheel
    $ twine upload dist/*
