TRASHTALK
=========

*Script to simplify trash gestion*

.. image:: https://travis-ci.org/PTank/trashtalk.svg?branch=master
    :target: https://travis-ci.org/PTank/trashtalk

.. image:: https://coveralls.io/repos/github/PTank/trashtalk/badge.svg?branch=master
    :target: https://coveralls.io/github/PTank/trashtalk?branch=master

Install
-------

::

    pip install trashtalk
    # or manually
    git clone git@github.com:PTank/trashtalk.git
    cd trashtalk
    python setup.py install

Usage
-----

.. code-block:: bash

    trashtalk # with any argument return path to trash
    trashtalk -cl # clean all files in trash
    trashtalk -l -s # -l list files in trash -s add size info
    trashtalk -f # you can tab file from selected trash, use with options (cl, l, s, i, re)
    # you can select multiple trash
    trashtalk -h # for more info

.trashtalk
----------

You can write a '.trashtalk' file on your home for help your trash usage

::

    # this is a comment
    TRASH_PATH=direct/path/to/trash , name_of_this_trash
    MEDIA_PATH=path/of/your/medias
    # you can add multiple path
