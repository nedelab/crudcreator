
Contributing
===================

The community welcomes your contributions to CRUDCreator!

Create your development environment
--------------------------------------------

If you'd like to contribute to CRUDCreator, you'll first need to create a local development and test environment.

*

    You will first need to clone the CRUDCreator git repository on your machine:

    .. code-block:: bash

        git clone https://github.com/nedelab/crudcreator.git

* 

    In the cloned folder, create a new Python virtual environment:

    .. code-block:: bash

        cd crudcreator
        python -m venv env

* 

    Then activate the Python virtual environment:

    On a Unix bash :

    .. code-block:: bash

        . ./env/bin/activate

    On Powershell :
        
    .. code-block:: bash
    
        ./env/Scripts/activate.ps1

* Then install the requirements :

    .. code-block:: bash

        pip install -r requirements.txt
    

Let's get started! You're ready to develop on CRUDCreator!

Tests
--------------------------------------------

To simplify testing, we recommend that you have Docker installed locally on your machine. If this isn't the case, it's not a problem - you'll just have to do a bit more work to configure the tests.


Start the postgres test database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**With Docker**

If you are using the solution with Docker, please follow the steps below:

* Start your deamon docker.

* 
    Start the postgres container that will be our test base:

    .. code-block:: bash

        cd test/data/postgres
        . ./start_dev.ps1



**Without Docker**

If you don't have Docker installed on your machine, you'll need to manually install a postgres on it, and configure it so that the config test/setting/postgres.json allows you to connect to it.

.. _manual_testing:

Manual testing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can then start the API and test it manually:

.. code-block:: bash

    python .\start_app_test.py <CRUDCREATOR_TEST_ENV>

With CRUDCREATOR_TEST_ENV one of the following values :

* async_postgres
* postgres

The possible values for CRUDCREATOR_TEST_ENV are the names of the config files in the test/settings folder.



Launch unit tests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To run unit tests in your environment :

*
    .. code-block:: bash

            python .\run_test.py <CRUDCREATOR_TEST_ENV>

    With CRUDCREATOR_TEST_ENV the same as in the above section (:ref:`manual_testing`)


Launch unit tests in dockers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The "test/docker" folder contains a set of docker configurations for testing crudcreator with different types of environment (for example, testing crudcreator on different versions of Python and SQLAlchemy).

To launch one of these tests, you must :

* 
    go to the project root (do not enter "test")

* 
    start one of the "run_test.ps1" files. For example :

    .. code-block:: bash

        . ./test/docker/python3.12/run_test.ps1

The folder also contains a number of items for testing the installation and scripts in a docker :

.. code-block:: bash

        . ./test/docker/installation/run_test.ps1

Contributor License Agreement (CLA)
--------------------------------------------

At the time of your pull request, you will be asked to sign a Contributor License Agreement (CLA).
