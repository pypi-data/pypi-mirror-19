Gitql 
====================

.. image:: https://travis-ci.org/mackong/gitql.svg?branch=master
   :target: https://travis-ci.org/mackong/gitql

Gitql is a Git query language.

Gitql is written in Golang by
`cloudson <https://github.com/cloudson/gitql>`__ originally, I
reimplemented by python language, and with some enhancements.

Installation
------------
::

    pip install gitql

or

::

    pip install git+https://github.com/mackong/gitql.git#egg=gitql

or

::

    python setup.py install

Usage
-----

::

    usage: gitql [-h] [-i] [-p PATH] [-s] [-t {table,json}] [-f] [-v] [SQL]

    Git query language

    positional arguments:
      SQL                   A query to run

    optional arguments:
      -h, --help            show this help message and exit
      -i, --interactive     Enter to interactive mode
      -p PATH, --path PATH  The path to run gitql (default ".")
      -s, --show-tables     Show all tables
      -t {table,json}, --type {table,json}
                            The output type format (default "table")
      -f, --format-json     Format the json output
      -v, --version         Show the version of gitql

Compare to `Gitql <https://github.com/cloudson/gitql>`__
--------------------------------------------------------

-  tables, fields, keywords **case-insensitive**

   ::

       Select * From COMMITS wherE author='bob';

-  field message -> summary, full\_message -> message changed in commits
   table

-  \* can combined with other fields

   ::

       select *, name, full_name from tags;

-  a table footer added similar to **mysql**

-  keyword **NOT** added

   ::

       select * from tags where not 'RC' in name;

-  limit -1 for **all** records

   ::

       select * from tags limit -1;

-  offset added to limit

   ::

       select * from tags limit 5, 5;

   or

   ::

       select * from tags limit 5 offset 5;

-  tailing ``;`` is optional

   ::

       select * from tags

   or

   ::

       select * from tags;

-  value type limitation in where clause removed

   ::

       select summary, date from commits where '2016-12-28' < date;

   or

   ::

       select * from commits where 1 and 2;
