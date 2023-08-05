Camo sign
#########

.. image:: https://travis-ci.org/BKNO3/camo-sign.svg?branch=master
    :target: https://travis-ci.org/BKNO3/camo-sign


Create signed URLs for use with camo_.

.. _camo: https://github.com/atmos/camo


Installation
============

::

    pip install camo-sign


Example usage
=============

.. code-block:: python

    >>> base_url = 'https://camo.example.com/'
    >>> secret_key = b'OMGWTFBBQ'
    >>> image_url = 'http://example.com/img.jpg'

    >>> create_signed_url(base_url, secret_key, image_url)
    https://camo.example.com/22fd0910eeefa6db9d4b105aa92c56d09bccf05f/687474703a2f2f6578616d706c652e636f6d2f696d672e6a7067'
