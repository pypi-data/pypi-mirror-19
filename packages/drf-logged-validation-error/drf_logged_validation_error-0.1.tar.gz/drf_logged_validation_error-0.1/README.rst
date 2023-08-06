Django REST Framework Logged Validation Error
=============================================

Raise validation with log in Django REST Framework API.

Install
-------

Use :code:`pip` to install.

    $ pip install drf-logged-validation-error

Usage
-----

Use :code:`logged_validation_info`, :code:`logged_validation_warning`, or :code:`logged_validation_error`
in your serializer validation process when you want to raise :code:`ValidationError`.
Choose logger according to the flag level you prefer to have with the :code:`ValidationError`.

.. code-block:: python

    from drf_logged_validation_error import logged_validation_info, logged_validation_warning, logged_validation_error

