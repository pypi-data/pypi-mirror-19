cpauto
======

|PyPI|

|Build Status|

cpauto is a client library, written in Python, for the web APIs exposed
via Check Point R80 management server software. The Check Point R80
management APIs provide automation and integration capabilities that
were not available in previous versions of Check Point management server
software.

https://sc1.checkpoint.com/documents/R80/APIs/#introduction

Behold, the power of cpauto:

::

    >>> import cpauto
    >>> cc = cpauto.CoreClient('admin', 'vpn123', '10.6.9.81')
    >>> r = cc.login()
    >>> r.status_code
    200
    >>> r.json()
    {u'last-login-was-at': {u'posix': 1478636363481, u'iso-8601': u'2016-11-08T15:19-0500'}, u'uid': ...}
    >>> n = cpauto.Network(cc)
    >>> r = n.add('net_mgmt', { 'subnet': '10.6.9.0', 'subnet-mask': '255.255.255.0' })
    >>> r.status_code
    200
    >>> r.json()
    {u'domain': {u'domain-type': u'domain', u'name': u'SMC User', u'uid': u'41e821a0-3720-11e3-aa6e-0800200c9fde'}, ...}
    >>> r = cc.publish()
    >>> r.status_code
    200
    >>> r.json()
    {u'task-id': u'01234567-89ab-cdef-8b0a-92e9635a47d3'}
    >>> r = cc.logout()
    >>> r.status_code
    200
    >>> r.json()
    {u'message': u'OK'}

Installation
============

To install cpauto, simply:

::

    $ pip install cpauto

Enjoy.

Documentation
=============

|Documentation Status|

Copious documentation is available at: http://cpauto.readthedocs.io/

.. |PyPI| image:: https://img.shields.io/pypi/v/cpauto.svg
   :target: https://pypi.python.org/pypi/cpauto
.. |Build Status| image:: https://travis-ci.org/dana-at-cp/cpauto.svg?branch=master
   :target: https://travis-ci.org/dana-at-cp/cpauto
.. |Documentation Status| image:: https://readthedocs.org/projects/cpauto/badge/?version=latest
   :target: http://cpauto.readthedocs.io/en/latest/?badge=latest


.. :changelog:

Release History
---------------

0.0.5 (2017-01-31)
++++++++++++++++++

**New Features**

- Full support for threat profiles.

**Bug Fixes**

- Fixed issue discovered in the wait for task logic.

0.0.4 (2016-12-09)
++++++++++++++++++

**New Features**

- Full support for sessions.
- The core client now optionally waits for tasks.

**Miscellaneous**

- Documentation is updated and hosted via readthedocs.io.

0.0.3 (2016-11-23)
++++++++++++++++++

**New Features**

- Full support for service and application objects.

**Miscellaneous**

- All code confirmed to work with Python versions 2.7, 3.5, and in between.

0.0.2 (2016-11-21)
++++++++++++++++++

**New Features**

- Full support for access and NAT objects.
- Support for some misc. powerful features.

0.0.1 (2016-11-15)
++++++++++++++++++

**Features**

- Full support for policy package, simple gateway, host, group and network objects.


