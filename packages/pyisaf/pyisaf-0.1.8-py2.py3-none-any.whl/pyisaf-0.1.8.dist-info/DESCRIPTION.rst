=======
pyisaf
=======

.. image:: https://img.shields.io/pypi/v/pyisaf.svg
        :target: https://pypi.python.org/pypi/pyisaf

.. image:: https://img.shields.io/travis/versada/pyisaf.svg
        :target: https://travis-ci.org/versada/pyisaf

.. image:: https://codecov.io/gh/versada/pyisaf/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/versada/pyisaf

Python library for i.SAF VAT report generation.


* GitHub: https://github.com/versada/pyisaf
* Free software: BSD license
* Supported Python versions: 2.7, 3.5+

Features
--------

* i.SAF data validation based on XSD
* i.SAF XML builder

Usage
-----

A complete example of i.SAF data dict can be found `in the tests
<https://github.com/versada/pyisaf/blob/master/tests/data.py>`_.

.. code:: python

    from pyisaf import schema_v1_2 as isaf_schema, ISAF1_2Builder as Builder
    from schema import SchemaError


    # Prepare i.SAF data
    data = {
        'header': {
            'file_description': {
                # ...
            },
        },
        'master_files': {
            'customers': {
                # ...
            },
            'suppliers': {
                # ...
            },
        },
        'source_documents': {
            'purchase_invoices': {
                # ...
            },
            'sales_invoices': {
                # ...
            },
            'settlements_and_payments': {
                # ...
            },
        },
    }
    # Validate data against i.SAF schema
    isaf_data = isaf_schema.validate(data)

    # Build the XML
    builder = Builder(isaf_data)
    isaf_xml = builder.dumps()


.. :changelog:

History
-------

v0.1.8 (2017-02-01)
~~~~~~~~~~~~~~~~~~~

* Updates links after repository transfer.

v0.1.7 (2017-01-24)
~~~~~~~~~~~~~~~~~~~

* Fixes rendering of elements which are nillable to set xsi:nil attribute

v0.1.6 (2017-01-06)
~~~~~~~~~~~~~~~~~~~

* Adds Python 3.6 build

v0.1.5 (2016-12-05)
~~~~~~~~~~~~~~~~~~~

* Fixes to not add empty tags like Customers, Suppliers, PurchaseInvoices if
  the underlying collection is empty.

v0.1.4 (2016-11-30)
~~~~~~~~~~~~~~~~~~~

* Fixes nillable dates rendering

v0.1.3 (2016-11-24)
~~~~~~~~~~~~~~~~~~~

* Includes packages (fail)
* Removes docs from the packages

v0.1.2 (2016-11-24)
~~~~~~~~~~~~~~~~~~~

* Minor fixes in description

v0.1.1 (2016-11-24)
~~~~~~~~~~~~~~~~~~~

* Initial version


