
.. _simple_example:

First simple example
============================

Introduction
-------------------------------

This example is one of the simplest you can create.

The CRUD interface on which we wish to interface is an SQLite database, which contains only a "book" table.

We want to turn it into a REST interface that implements a simple CRUD.


Set up the example
-------------------------------

If you come from :ref:`getting_started`, you can skip the setup section.

.. code-block:: bash

    mkdir crudcreator_test
    cd crudcreator_test
    python -m venv env
    ./env/bin/activate
    crudcreator init simple
    pip install -r requirements.txt


Run the example
-------------------------------

.. code-block:: bash

   ./env/bin/activate

   python ./reinit_db.py

   python ./main.py

Then open your web browser and go to http://127.0.0.1:8000/docs: you'll see the REST API swagger created by crudcreator.

Explanations
-------------------------------

CRUDCreator has created 4 REST routes associated with the "book" entity:

* a GET /book route, which corresponds to the CRUD's "Read".

* a POST /book route, corresponding to the CRUD's "Create".

* a DELETE /book route, corresponding to the CRUD's "Delete".

* a PATCH /book route, corresponding to the CRUD's "Update".


We have defined the "book" entity in the "descriptors/book.json" file.

We created the REST API associated with this entity with the following lines of code in main.py :

.. code-block:: python

    ...
    build_read(crud_object, transaction_manager)#add a route for the Read (GET)
    build_create(crud_object, transaction_manager)#add a route for Create (POST)
    build_delete(crud_object, transaction_manager)#add a route for Delete (DELETE)
    build_update(crud_object, transaction_manager)#add a route for Update (PATCH)
    ...

For more details, see the builder doc here : :ref:`builder`.

Read
~~~~~~~~~~

The GET route returns the list of books contained in the database.

If the user calls the route, without filtering, he will receive a list containing two "book" entities.

Filters
^^^^^^^^^^

Our GET route can be filtered by book title. The API will then return a list of books whose title contains what was typed in the filter (this is a "contain" filter). If the user types "Bergerac", the route will return a list of a single element, containing the book whose title is "Cyrano de Bergerac".

CRUDCreator offers several types of filter. But in our definition of the "book" entity, in the "book.json" file, we chose a "contain" filter. We could have defined an "equal" filter for an exact search, or a "pattern" filter to allow searches like "%Lords%Ring%Tome _" ("%" for "any number of character" and "_" for "one character"). There are many other types of filtration, as we'll see in other examples.

Filters are defined by adding a "FilterFirewall" proxy to our "book.json" file:

.. code-block:: json

   {
        "name": "FilterFirewall",//the name of the proxy (see doc for a list of available proxies)
        "params": {
            "allowed_filter_on_fields": [//a list of allowed filters (here only one, to keep it simple)
                {
                    "field_name": "title",//the field on which the user can filter
                    "allowed_filter_type": {
                        "filtration_type": "contain",//a "contain" type filter, which returns books whose title contains the searched value
                        "is_mandatory": false,//the filter is not mandatory
                        "default": null
                    }
                }
            ]
        }
    }

    
For more details, see the proxy doc here : :ref:`filter_firewall`.

.. note::

    Notice that, on the swagger, the GET route description has been automatically generated. In particular, it describes the different allowed filters, and their type ("contain", "equal", "pattern", "different", etc).

Types
^^^^^^^^^^

When we described the "book" entity, in the "book.json", notice that nowhere did we define the types of the entity's fields. CRUDCreator guessed on his own that "book_id" is an int, "title" a str and "public_domain" a boolean. He fetched the information directly from our SQL database.

The types are documented in the swagger.

Crudcreator even guessed that "title" was limited to 100 characters, and reflected this in the REST API definition. This constraint on "title" is also visible in the swagger.

Of course, it is possible to overwrite types (if, for example, you wish to transform a str into a bool). But we'll look at that in another example. (For those in a hurry, see the RecastType proxy doc here: :ref:`recast_type`).

Other
^^^^^^^^^^

There are many other proxies available for customizing the GET route created by crudcreator:

* you can change field names to be different from SQL column names (:ref:`rename`);
* you can link two SQL tables to make a single entity on the REST interface. For example, the "book" table with an "author" table in a one-to-one, or a one-to-many relation, to have book and author info on the same route (:ref:`sql_link`);
* you can force certain filters. For example, a filter on a username retrieved from a JWT token, to return to the API user only those lines to which he has access rights (:ref:`add_filter`);
* etc (see :ref:`doc_proxy` for an exhaustive list).

We'll look at this in the next few examples.


Create
~~~~~~~~~~

The POST route allows the user to add a row to the "book" table.

The values of the book to be created are entered by the user in the request body, in json format.

Key uniqueness
^^^^^^^^^^^^^^^^^^^^^^

In the "book.json", we have defined the "book_id" field as the entity identifier. If we try to create a book whose "book_id" is already taken by another book in the database, the REST API will return a "409 Conflict" code.

Note that the REST API blocks the creation and returns a 409 error even if "book_id" has not been defined as a primary key in our SQL database, and therefore even if it is theoretically possible to inject the same "book_id" into the database several times.

It is also possible to define several identifier fields on the same entity. The uniqueness constraint would then apply to the identifiers taken as a whole.

We have defined "book_id" as the entity identifier using the following lines in the "book.json" file:

.. code-block:: json

   {
        "name": "book_id",//the field name
        "is_id_field": true,//is it part of the identifier?
        "can_be_created": true,//can the user specify a value at creation?
        "can_be_updated": true//can the user modify the value after creation?
    }

If "is_id_field" had not been specified in the "book.json", crudcreator would have fetched the information from the SQL database. If the field is a primary key in the SQL database, crudcreator would have defined the field as an identifier.

Other
^^^^^^^^^^

There are many other proxies available for customizing the POST route created by crudcreator:

* field names can be changed to differ from SQL column names (:ref:`rename`);
* you can force certain values. For example, a value equal to the username retrieved from a JWT token, to indicate who is the owner of the created line, and therefore who will have the right to read or modify it. Or a "creation_date" (:ref:`add_write_value`).
* linked entities can be created in cascade (:ref:`cascade_create_and_update`);
* etc (see :ref:`doc_proxy` for an exhaustive list).

We'll look at this in the next examples.


Delete
~~~~~~~~~~

The DELETE route allows the user to delete a row from the "book" table.

The line deleted is the one associated with the identifier sent as a route parameter.

Existence of the entity
^^^^^^^^^^^^^^^^^^^^^^^^^^

If the identifier given as a route parameter is not associated with any entity, the route returns a "404 Not Found" error.

Other
^^^^^^^^^^

There are many other proxies available for customizing the DELETE route created by crudcreator:

* field names can be changed to differ from SQL column names (:ref:`rename`);
* you can configure a "soft delete". In this case, crudcreator won't delete the row from the database, but will instead assign a value to a column indicating that the row has been deleted (for example, an "is_deleted" or "deletion_date" column). The row will then not appear in the GET, even if it is still present in the database (:ref:`soft_delete`);
* certain identifiers can be forced. For example, an identifier equal to the username retrieved from a JWT token, to indicate who is the owner of the line to be deleted. Prevent users from deleting lines they don't own (:ref:`add_id_value`);
* linked entities can be deleted in cascade (:ref:`cascade_delete`);
* etc (see :ref:`doc_proxy` for an exhaustive list).

We'll look at this in the next examples.


Update
~~~~~~~~~~

The PATCH route allows the user to modify a line in the "book" table.

The modified line is the one associated with the identifier sent as a route parameter.

The new book values are entered by the user in the query body, in json format. If a field is not to be modified, simply don't provide it in the json.

Entity existence
^^^^^^^^^^^^^^^^^^^^^^^^^^

If the identifier given as a route parameter is not associated with any entity, the route returns a "404 Not Found" error.

Key uniqueness
^^^^^^^^^^^^^^^^^^^^^^

If the user tries to give the book a new "book_id", and this is already taken by another book in the database, the REST API will return a "409 Conflict" code. In this way, identifiers remain unique.

Other
^^^^^^^^^^

There are many other proxies available for customizing the PATCH route created by crudcreator:

* field names can be changed to differ from SQL column names (:ref:`rename`);
* you can force certain identifiers. For example, an identifier equal to the username retrieved from a JWT token, to indicate who is the owner of the line to be modified. Prevent users from modifying lines for which they are not the owner (:ref:`add_id_value`);
* In the same way, certain values can be forced. For example, a "last_modification_date" (:ref:`add_write_value`);
* linked entities can be created in cascade (:ref:`cascade_create_and_update`);
* etc (see :ref:`doc_proxy` for an exhaustive list).

We'll look at this in the next examples.


Run the unit tests in the example
--------------------------------------------------------------

To run the unit tests of the example :

.. code-block:: bash

   pip install pytest pytest-asyncio httpx

   pytest test