Plone hotfix, 2017-01-17
========================

This hotfix fixes several security issues:

- A reflected Cross Site Scripting attack (XSS) in the ZMI (``manage_findResult``).
  You may already be blocking access to ``manage`` pages in a web server like ``nginx`` or ``Apache``.
  In that case, this part of the hotfix is fine, but is not relevant.

- Accessing private content via ``str.format`` in through-the-web templates and scripts.
  See this `blog post by Armin Ronacher <http://lucumr.pocoo.org/2016/12/29/careful-with-str-format/>`_ for the general idea.
  Since the ``format`` method was introduced in Python 2.6, this part of the hotfix is only relevant for Plone 4 and 5, not Plone 3.


Compatibility
=============

This hotfix should be applied to the following versions of Plone:

* Plone 5.0.6 and any earlier 5.x version
* Plone 4.3.11 and any earlier 4.x version
* Any older version of Plone

The hotfix is officially supported by the Plone security team on the
following versions of Plone in accordance with the Plone
`version support policy`_: 4.0.10, 4.1.6, 4.2.7, 4.3.11 and 5.0.6.
However it has also received some testing on older versions of Plone.
The fixes included here will be incorporated into subsequent releases of Plone,
so Plone 4.3.12, 5.0.7 and greater should not require this hotfix.


Installation
============

Installation instructions can be found at
https://plone.org/security/hotfix/20170117


Automated testing
=================

If you have automated tests for your code and you want to run them in combination with this hotfix, to see if there any regressions, you should make sure the hotfix is included in your test setup.
With plone.app.testing it should look something like this in your test layer fixture::


    def setUpZope(self, app, configurationContext):
        from plone.testing import z2
        z2.installProduct(app, 'Products.PloneHotfix20170117')

With the old-style Products.PloneTestCase it should be like this::

    from Testing import ZopeTestCase
    ZopeTestCase.installProduct('PloneHotfix20170117', quiet=1)


Q&A
===

Q: How can I confirm that the hotfix is installed correctly and my site is protected?
  A: On startup, the hotfix will log a number of messages to the Zope event log
  that look like this::

      2017-01-17 08:42:11 INFO Products.PloneHotfix20170117 Applied zmi patch
      2017-01-17 08:42:11 INFO Products.PloneHotfix20170117 Hotfix installed

  The exact number of patches applied, will differ depending on what packages you are using.
  If a patch is attempted but fails, it will be logged as a warning that says
  "Could not apply". This may indicate that you have a non-standard Plone
  installation.

Q: How can I report problems installing the patch?
  A: Contact the Plone security team at security@plone.org, or visit the
  #plone channel on freenode IRC.

Q: How can I report other potential security vulnerabilities?
  A: Please email the security team at security@plone.org rather than discussing
  potential security issues publicly.

.. _`version support policy`: http://plone.org/support/version-support-policy
