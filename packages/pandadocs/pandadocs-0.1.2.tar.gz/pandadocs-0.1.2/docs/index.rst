.. pandadocs documentation master file, created by
   sphinx-quickstart on Tue Jul  9 22:26:36 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pandadoc's documentation!
======================================

Pandadoc_ is a great way to integrate digital signatures in your application. This python package, brought to you by `Alokin Software`_, provides the Pandadoc REST API in an easy pythonic form. It's a simple implementation using python requests and its OAuth extension.

Also included is the pandadocs-tokentool wizard that helps you generate access tokens for use with server-side flows. It also serves as a good example for using the python module.

Here's an example of how to use the pandadocs API with this module::

    from pandadocs.api import Session


    client_id = 'a202d5bc3e2bc7fc420e'
    client_secret = '3e895239189456acfb339'
    auth_code = '26j4017252t49wfe0399'

    token = {
        u'access_token': u'54be934eb3fdf031ccadd2406f2',
        u'expires_at': 1499753835.037497,
        u'expires_in': 31535999,
        u'refresh_token': u'2x1dd5a32dtag90298c3b2214',
        u'scope': [u'read', u'write', u'read+write'],
        u'token_type': u'Bearer'
    }

    panda = Session(client_id=client_id, token=token)

    for t in panda.iter_templates_pages():
        print t.json()

.. _Pandadoc: https://developers.pandadoc.com/
.. _Alokin Software: http://alokin.in

.. toctree::
   :maxdepth: 2

   readme
   installation
   usage
   contributing
   authors
   history

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
