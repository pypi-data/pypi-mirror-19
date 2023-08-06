chembl_migrate
======


.. image:: https://img.shields.io/pypi/v/chembl_migrate.svg
    :target: https://pypi.python.org/pypi/chembl_migrate/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/dm/chembl_migrate.svg
    :target: https://pypi.python.org/pypi/chembl_migrate/
    :alt: Downloads

.. image:: https://img.shields.io/pypi/pyversions/chembl_migrate.svg
    :target: https://pypi.python.org/pypi/chembl_migrate/
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/status/chembl_migrate.svg
    :target: https://pypi.python.org/pypi/chembl_migrate/
    :alt: Development Status

.. image:: https://img.shields.io/pypi/l/chembl_migrate.svg
    :target: https://pypi.python.org/pypi/chembl_migrate/
    :alt: License

.. image:: https://badge.waffle.io/chembl/chembl_migrate.png?label=ready&title=Ready 
 :target: https://waffle.io/chembl/chembl_migrate
 :alt: 'Stories in Ready'

This is chembl_migrate package developed at Chembl group, EMBL-EBI, Cambridge, UK.

This package provides custom Django management command 'migrate'.
For usage type `python manage.py migrate help`.
'migrate' copies data from one database to another.
Both databases must be described by the same Django model.
By default django model being migrated is 'chembl_migration_model' but this can be changed in settings to any other django model.
If target database doesn't have tables required by the model they will be created, despite status of 'managed' meta flag.
All data is copied in order that should avoid any integration errors.
Migration process is done in chunks of 1000 records but this number can be configured.
Each chunk is copied within a transaction.
When interrupted, the migration process can be rerun and it will detect which data has already been migrated and start migration from the point where it finished.
