
SQL proxies
================

These proxies are only used when the source is a SQL database.
They build SQL queries, which are then executed by the SQLRequestExecutor module.
They must therefore be placed between the source and the generic (source-independent) proxies.

.. contents:: Contents
    :depth: 2
    :local:
    


Abstract classes
---------------------------

.. module:: crudcreator.adaptator.sql.proxy.AbstractSQLRequestProxy
    :noindex:

.. autopydantic_model:: AbstractSQLRequestProxy
    :members:
    :model-show-json: false
    :model-show-field-summary: false

|
|

.. autopydantic_model:: AbstractSQLRequestProxyParams
    :members:
    :model-show-json: false
    :model-show-field-summary: false


Concrete classes
---------------------------

SQLRequestConstructor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. module:: crudcreator.adaptator.sql.proxy.SQLRequestConstructor
    :noindex:

.. autopydantic_model:: SQLRequestConstructor
    :members:
    :model-show-json: false
    :model-show-field-summary: false

|
|

.. autopydantic_model:: SQLRequestConstructorParams
    :members:
    :model-show-json: false
    :model-show-field-summary: false

SQLFilter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. module:: crudcreator.adaptator.sql.proxy.SQLFilter
    :noindex:

.. autopydantic_model:: SQLFilter
    :members:
    :model-show-json: false
    :model-show-field-summary: false

|
|

.. autopydantic_model:: SQLFilterParams
    :members:
    :model-show-json: false
    :model-show-field-summary: false


SQLSort
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. module:: crudcreator.adaptator.sql.proxy.SQLSort
    :noindex:

.. autopydantic_model:: SQLSort
    :members:
    :model-show-json: false
    :model-show-field-summary: false

|
|

.. autopydantic_model:: SQLSortParams
    :members:
    :model-show-json: false
    :model-show-field-summary: false

|
|

.. autopydantic_model:: FieldToSort
    :members:
    :model-show-json: false
    :model-show-field-summary: false

|
|

.. autoclass:: SortType()
    :members:

SQLPagination
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. module:: crudcreator.adaptator.sql.proxy.SQLPagination
    :noindex:

.. autopydantic_model:: SQLPagination
    :members:
    :model-show-json: false
    :model-show-field-summary: false

|
|

.. autopydantic_model:: SQLPaginationParams
    :members:
    :model-show-json: false
    :model-show-field-summary: false


.. _sql_link:

SQLCreateLink
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. module:: crudcreator.adaptator.sql.proxy.SQLCreateLink
    :noindex:

.. autopydantic_model:: SQLCreateLink
    :members:
    :model-show-json: false
    :model-show-field-summary: false

.. _sql_read_from_link:

SQLReadFromLink
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. module:: crudcreator.adaptator.sql.proxy.SQLReadFromLink
    :noindex:

.. autopydantic_model:: SQLReadFromLink
    :members:
    :model-show-json: false
    :model-show-field-summary: false

|
|

.. autopydantic_model:: SQLReadFromLinkParams
    :members:
    :model-show-json: false
    :model-show-field-summary: false

|
|

.. autopydantic_model:: SQLActivateEntityOnlyOnOption
    :members:
    :model-show-json: false
    :model-show-field-summary: false


SQLRequestExecutor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. module:: crudcreator.adaptator.sql.proxy.SQLRequestExecutor
    :noindex:

.. autopydantic_model:: SQLRequestExecutor
    :members:
    :model-show-json: false
    :model-show-field-summary: false

|
|

.. autopydantic_model:: SQLRequestExecutorParams
    :members:
    :model-show-json: false
    :model-show-field-summary: false