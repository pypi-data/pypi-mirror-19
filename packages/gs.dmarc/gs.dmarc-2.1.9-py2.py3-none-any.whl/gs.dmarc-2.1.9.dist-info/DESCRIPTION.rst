============
``gs.dmarc``
============
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Look up and report on the DMARC status of a domain
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2015-06-25
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.net`_.

..  _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

Introduction
============

This product allows systems look up and report on the DMARC (`RFC
7489`_: Domain-based Message Authentication, Reporting and
Conformance) status of a domain. DMARC allows the owner of a
domain to publish a key that is used to verify if an email
message actually originated from the domain, and to publish what
to do if the verification fails. It is an extension of DKIM (`RFC
6376`_: DomainKeys Identified Mail) and SPF (`RFC 4408`_: Sender
Policy Framework).

Specifically this product supplies ``gs.dmarc.ReceiverPolicy``
for enumerating [#enum34]_ the different DMARC policies, and the
``receiver_policy`` function for querying the policy for a
given domain.

Resources
=========

- Documentation: http://gsdmarc.readthedocs.io/
- Code repository: https://github.com/groupserver/gs.dmarc
- Questions and comments to
  http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _RFC 7489: https://tools.ietf.org/html/rfc7489.html
.. _RFC 6376: http://tools.ietf.org/html/rfc6376
.. _RFC 4408: http://tools.ietf.org/html/rfc4408
.. [#enum34] `The enum34 package`_ is used to provide `Enum`_
           support for releases of Python prior to 3.4.
.. _The enum34 package: https://pypi.python.org//pypi/enum34
.. _Enum: https://docs.python.org/3/library/enum.html
.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17

..  LocalWords:  DMARC DKIM DomainKeys dkim groupserver spf enum
..  LocalWords:  lookup

Changelog
=========

2.1.9 (2016-12-16)
------------------

* Falling back to the either the overall subdomain-policy or
  overall domain-policy if a subdomain lacks a specific published
  DMARC record — with thanks to Igor Colombi for pointing out
  the issue

2.1.8 (2016-10-18)
------------------

* Adding :pep:`484` type hints
* Updating the public-suffix list
* Using :mod:`setuptools` to return the public-suffix list

2.1.7 (2016-04-11)
------------------

* Testing with Python 3.5
* Switching to dictionary-comprehensions

2.1.6 (2016-03-24)
------------------

* Updating the suffix list from Mozilla, thanks to `Baran
  Kaynak`_

.. _Baran Kaynak: https://github.com/barankaynak

2.1.5 (2015-09-01)
------------------

* Catching ``dns.resolver.NoNameserver`` exceptions, thanks to
  `Alexy Mikhailichenko`_

.. _Alexy Mikhailichenko: https://github.com/alexymik

2.1.4 (2015-06-25)
------------------

* Fixing a spelling mistake in the README, thanks to `Stefano
  Brentegani`_
* Updating the documentation, as DMARC is now :rfc:`7489`

.. _Stefano Brentegani: https://github.com/brente

2.1.3 (2014-10-20)
------------------

* Handling domains with invalid DMARC policies, closing `Bug 4135`_

.. _Bug 4135: <https://redmine.iopen.net/issues/4135

2.1.2 (2014-09-26)
------------------

* Switching to GitHub_ as the primary code repository.

.. _GitHub: https://github.com/groupserver/gs.dmarc

2.1.1 (2014-07-09)
------------------

* Coping when the host-name passed to ``lookup_receiver_policy``
  for hosts that start with ``_dmarc`` already
* Rejecting all answers that do not start with ``v=DMARC1``, as
  per `Section 7.1`_ (number 5) of the draft DMARC specification

.. _Section 7.1: https://tools.ietf.org/html/rfc7489#section-7.1

2.1.0 (2014-05-07)
------------------

* Adding ``gs.dmarc.receiver_policy``, which looks up the
  organisational domain
* Updating the Sphinx documentation

2.0.0 (2014-04-29)
------------------

* Adding ``gs.dmarc.ReceiverPolicy.noDmarc``, and returning it
  from ``gs.dmarc.lookup_receiver_policy``
* Adding Sphinx documentation

1.0.0 (2014-04-24)
------------------

Initial release.

..  LocalWords:  Changelog GitHub README


