chembl_business_model
======


.. image:: https://img.shields.io/pypi/v/chembl_business_model.svg
    :target: https://pypi.python.org/pypi/chembl_business_model/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/dm/chembl_business_model.svg
    :target: https://pypi.python.org/pypi/chembl_business_model/
    :alt: Downloads

.. image:: https://img.shields.io/pypi/pyversions/chembl_business_model.svg
    :target: https://pypi.python.org/pypi/chembl_business_model/
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/status/chembl_business_model.svg
    :target: https://pypi.python.org/pypi/chembl_business_model/
    :alt: Development Status

.. image:: https://img.shields.io/pypi/l/chembl_business_model.svg
    :target: https://pypi.python.org/pypi/chembl_business_model/
    :alt: License

.. image:: https://badge.waffle.io/chembl/chembl_business_model.png?label=ready&title=Ready 
 :target: https://waffle.io/chembl/chembl_business_model
 :alt: 'Stories in Ready' 

This is chembl_business_model package developed at Chembl group, EMBL-EBI, Cambridge, UK.

This package provides a django ORM model decorated with additional information about various aspects like searching and api exposing.
It also adds some application specific logic like what to do when the compound is saved.

The package uses 'chembl_core_model' as its base and declares new model by proxy inheritance.
This model is required when you want to create/update (write/modify) objects to database through ORM.
Core model intended only for read, with methods from this module you can also write.

This module defines also some application specific models (in meta.py file) which can be kept in separate db schema.
