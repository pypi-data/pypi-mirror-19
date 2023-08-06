.. image:: https://raw.githubusercontent.com/mindey/subfiles/master/misc/subfiles.png
    :alt: Subfiles Illustration
    :width: 100%
    :align: center

Purpose
-------

Introduce command ``subtypes`` to extract subtypes of files in a directory, so as to have a list of file **sub**-extensions appearing in directory. 

Usage
-----

Set up::

    $ pip install subfiles

In any project, or directory, run to preview what files with subextensions are::

    $ subtypes -l <level>

    $ subtypes -s <level>

This will output files grouped by different file sub-extensions in the project. The default ``<level>=2``. You can output standard extensions by choosing ``<level>=1``.

To start defining more information for files with some file subtypes, do::

    $ subtypes -s > .subtypes

Then, edit the generated ``.subtypes`` file to suit your needs, in the following format:

The basic format of the .subfiles is a wildcard map of file extensions within a ``[]``, an optional short description after a hyphen surrounded by spaces, more information, and a new-line separator between the diffrent file format descriptions, that is:

.. code::

   [*.my_type.csv] - SHORT DESCRIPTION
   MORE INFORMATION

   [*.my_other_type.json] - SHORT DESCRIPTION
   MORE INFORMATION

Usage to Encode Schemas
-----------------------
One very useful case for ``.subtypes``, is encoding the information about the data schemas stored in files with sub-extensions. For this use-case, we might even agree to use a special kind of subtype, which is ``.schema.subtypes``:

.. code::

   [*.graph.json] - https://www.wikidata.org/wiki/Q182598
   cat: https://www.wikidata.org/wiki/Q146
   dog: https://www.wikidata.org/wiki/Q144
   love: https://www.wikidata.org/wiki/Q316
   
   [*.products.csv] - https://www.wikidata.org/wiki/Q278425
   url: https://www.wikidata.org/wiki/Q42253
   currency: https://www.wikidata.org/wiki/Q8142
   price: https://www.wikidata.org/wiki/Q160151
   name: https://www.wikidata.org/wiki/Q1786779

In the schema subtypes we could agree to have the links to concepts, the instance of which the thing in the file of this subextension is.

Custom Schemas
--------------

It may be that you are not entirely satisfied with the schema provided by http://schema.org, e.g., or want to define your own schemas in terms of concepts from custom or other ontologies, you could simply include them as a file subtype in your project.


Why?
----

The idea here is that our file extensions don't have to end with one dot, and we can create multi-level namespaces for file extensions for all kind of uses based on dot notation. There are many potential uses. For example, you might want to use secondary level extensions represent and map files with schemas of data instances that they contain. Why this matters for all data - https://youtu.be/KawiP8XBgtE .

So, the idea here is to introduce a ``.subtypes`` dot file to contain any metadata that data developer assumes for files with subextensions to carry beyond what the traditional file extension represents to help any other programs or humans to understand the files in any project.

The ``subtypes`` command is simply a helper to extract **subtypes of files** in a directory, so as to have a list of file "subextensions" appearing in directory for any purpose. A subextension is an extension of second or greater level (e.g., ``'hello.world.txt'`` has top level extension ``.txt``, and second level subextension ``.world``).

Development reminder
====================

To publish new version on PyPI::

    $ python setup.py sdist bdist_wheel
    $ twine upload dist/*
