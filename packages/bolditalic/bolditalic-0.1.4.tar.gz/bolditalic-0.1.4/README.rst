==========
bolditalic
==========

.. image:: https://travis-ci.org/kallimachos/bolditalic.svg?branch=master
   :target: https://travis-ci.org/kallimachos/bolditalic

.. image:: https://img.shields.io/pypi/status/bolditalic.svg?style=flat
   :target: https://pypi.python.org/pypi/bolditalic

.. image:: https://img.shields.io/pypi/v/bolditalic.svg?style=flat
   :target: https://pypi.python.org/pypi/bolditalic

.. image:: https://img.shields.io/badge/Python-2.7-brightgreen.svg?style=flat
   :target: http://python.org

.. image:: https://img.shields.io/badge/Python-3.4-brightgreen.svg?style=flat
   :target: http://python.org

.. image:: http://img.shields.io/badge/license-GPL-blue.svg?style=flat
   :target: http://opensource.org/licenses/GPL-3.0

.. warning::

   This extension is deprecated. Please use the bolditalic extension provided
   in the `chios package <https://pypi.python.org/pypi/chios>`_.

**bolditalic** is an extension for Sphinx that enables inline bold + italic
text styling.

Full documentation: https://kallimachos.github.io/bolditalic/


Installation
~~~~~~~~~~~~

Install **bolditalic** using ``pip``:

.. code::

   $ pip install bolditalic


Usage
~~~~~

#. Add **bolditalic** to the list of extensions in ``conf.py``:

   .. code::

      extensions = ['bolditalic']

#. Use the ``bolditalic`` role to style text:

   .. code::

      The end of this sentence :bolditalic:`displays in bold and italic`.
