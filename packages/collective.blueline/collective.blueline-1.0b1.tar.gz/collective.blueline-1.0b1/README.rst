********
Blueline
********

.. contents:: Table of Contents

Life, the Universe, and Everything
==================================

This package defines some helper viewlets to easily insert code on the layout of a Plone site.

One use case is the insertion of ad code from sites like DoubleClick.

The name comes from the `blue-line process`_, a document reproduction produced by using the diazo chemical process.
You already know the rest of the story.

.. _`blue-line process`: https://en.wikipedia.org/wiki/Whiteprint

Mostly Harmless
===============

.. image:: https://secure.travis-ci.org/simplesconsultoria/collective.blueline.png?branch=master
    :alt: Travis CI badge
    :target: http://travis-ci.org/simplesconsultoria/collective.blueline

.. image:: https://coveralls.io/repos/simplesconsultoria/collective.blueline/badge.png?branch=master
    :alt: Coveralls badge
    :target: https://coveralls.io/r/simplesconsultoria/collective.blueline

.. image:: https://pypip.in/d/collective.blueline/badge.png
    :alt: Downloads
    :target: https://pypi.python.org/pypi/collective.blueline/

Got an idea? Found a bug? Let us know by `opening a support ticket`_.

.. _`opening a support ticket`: https://github.com/simplesconsultoria/collective.blueline/issues

Don't Panic
===========

Installation
------------

To enable this package in a buildout-based installation:

#. Edit your buildout.cfg and add add the following to it::

    [buildout]
    ...
    eggs =
        collective.blueline

After updating the configuration you need to run ''bin/buildout'', which will take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to ``collective.blueline`` and click the 'Activate' button.

Usage
-----

TBD.
