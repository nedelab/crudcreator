.. _getting_started:

Getting started
=======================================

.. contents:: Contents
    :depth: 2
    :local:


Installation
----------------------

Prepare a test environment:

    .. highlight:: bash
    .. code-block:: bash

        mkdir crudcreator_test
        cd crudcreator_test
        python -m venv env
        ./env/bin/activate

Then install crudcreator with pip :

    .. highlight:: bash
    .. code-block:: bash

        pip install crudcreator


Skeleton creation
------------------------------------

CRUDCreator publishes a command to create the files required for startup. In the python environment where crudcreator is installed, run the following command :

    .. highlight:: bash
    .. code-block:: bash

        crudcreator init simple

Then :

    .. highlight:: bash
    .. code-block:: bash

        pip install -r requirements.txt

You'll then see a set of files and folders. The example ":ref:`simple_example`" details the files created.