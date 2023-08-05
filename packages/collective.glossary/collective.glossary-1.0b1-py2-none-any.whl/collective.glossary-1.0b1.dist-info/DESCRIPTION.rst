***************
Glossary
***************

.. contents:: Table of Contents

Life, the Universe, and Everything
==================================

A Dexterity-based content type to define a glossary and its terms.

This package is inspired in `PloneGlossary`_.

.. _`PloneGlossary`: https://pypi.python.org/pypi/Products.PloneGlossary

Mostly Harmless
===============

.. image:: http://img.shields.io/pypi/v/collective.glossary.svg
    :target: https://pypi.python.org/pypi/collective.glossary

.. image:: https://img.shields.io/travis/collective/collective.glossary/master.svg
    :target: http://travis-ci.org/collective/collective.glossary

.. image:: https://img.shields.io/coveralls/collective/collective.glossary/master.svg
    :target: https://coveralls.io/r/collective/collective.glossary

Got an idea? Found a bug? Let us know by `opening a support ticket`_.

.. _`opening a support ticket`: https://github.com/collective/collective.glossary/issues

Don't Panic
===========

Installation
------------

To enable this package in a buildout-based installation:

#. Edit your buildout.cfg and add add the following to it::

    [buildout]
    ...
    eggs =
        collective.glossary

After updating the configuration you need to run ''bin/buildout'', which will take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to ``collective.glossary`` and click the 'Activate' button.

Usage
-----

TBD.


Screenshots
-----------

.. figure:: https://raw.github.com/collective/collective.glossary/master/docs/glossary.png
    :align: center
    :height: 640px
    :width: 768px

    Create a Glossary.

.. figure:: https://raw.github.com/collective/collective.glossary/master/docs/usage.png
    :align: center
    :height: 640px
    :width: 768px

    Use it!

.. figure:: https://raw.github.com/collective/collective.glossary/master/docs/controlpanel.png
    :align: center
    :height: 400px
    :width: 768px

    The tooltip can be disabled in the control panel configlet.

Developer Notes
---------------

The terms are loaded in a page using an AJAX call to a browser view that returns them as a JSON object.

The tooltips will only be available in the default view of a content type instance.

Share and Enjoy
===============

This package would not have been possible without the contribution of the following people:

- Héctor Velarde
- Rodrigo Ferreira de Souza
- Font Awesome (`icons`_)

You can find an updated list of package contributors on `GitHub`_.

.. _`GitHub`: https://github.com/collective/collective.glossary/contributors
.. _`icons`: http://fortawesome.github.io/Font-Awesome/icons/

Changelog
=========

1.0b1 (2016-12-19)
------------------

- Term template was refactored to avoid duplicated definitions (closes `#26`_)
  [hvelarde]

- Glossary terms now use ``tile`` scales (closes `#5`_).
  [hvelarde]

- Remove dependency on five.grok.
  [hvelarde]

- Fix ``ReferenceError`` on JavaScript code (Plone 5 does not include global variables anymore).
  [hvelarde, rodfersou]

- Remove dependency on Products.CMFQuickInstallerTool.
  [hvelarde]

- Change glossary to always call JSON view from the portal URL (closes `#22`).
  [rodfersou]

- A new rich text field was added to the Glossary content type.
  [hvelarde]

- Normalize glossary index (closes `#18`_).
  [rodfersou]

- Add option to select content types that will display glossary terms (closes `#14`_).
  [rodfersou]

- Apply Glossary just to #content-core. (closes `#12`_).
  [rodfersou]

- Review method `is_view_action` to work with Virtual Host configuration.
  [rodfersou]

- Terms should only be added inside a Glossary (closes `#8`_).
  [hvelarde]


1.0a1 (2015-05-18)
------------------

- Initial release.

.. _`#5`: https://github.com/collective/collective.cover/issues/5
.. _`#8`: https://github.com/collective/collective.cover/issues/8
.. _`#12`: https://github.com/collective/collective.cover/issues/12
.. _`#14`: https://github.com/collective/collective.cover/issues/14
.. _`#18`: https://github.com/collective/collective.cover/issues/18
.. _`#22`: https://github.com/collective/collective.cover/issues/22
.. _`#26`: https://github.com/collective/collective.cover/issues/26


