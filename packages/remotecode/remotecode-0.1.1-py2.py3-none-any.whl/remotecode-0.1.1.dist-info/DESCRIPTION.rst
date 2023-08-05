==========
remotecode
==========

.. image:: https://travis-ci.org/kallimachos/remotecode.svg?branch=master
   :target: https://travis-ci.org/kallimachos/remotecode

.. image:: https://img.shields.io/pypi/status/remotecode.svg?style=flat
   :target: https://pypi.python.org/pypi/remotecode

.. image:: https://img.shields.io/pypi/v/remotecode.svg?style=flat
   :target: https://pypi.python.org/pypi/remotecode

.. image:: https://img.shields.io/badge/Python-2.7-brightgreen.svg?style=flat
   :target: http://python.org

.. image:: https://img.shields.io/badge/Python-3.4-brightgreen.svg?style=flat
   :target: http://python.org

.. image:: http://img.shields.io/badge/license-GPL-blue.svg?style=flat
   :target: http://opensource.org/licenses/GPL-3.0

.. warning::

   This extension is deprecated. Please use the remotecode extension provided
   in the `chios repository <https://github.com/kallimachos/chios>`_.

**remotecode** is an extension for Sphinx that enables code blocks from
remote sources.

Full documentation: https://kallimachos.github.io/remotecode/


Installation
~~~~~~~~~~~~

Install **remotecode** using ``pip``:

.. code::

   $ pip install remotecode


Usage
~~~~~

#. Add **remotecode** to the list of extensions in ``conf.py``:

   .. code::

      extensions = ['remotecode']

#. Use the ``remote-code-block`` directive to fetch remote source code and
   display it in a ``code-block``.

   .. code::

      .. remote-code-block:: ini

         https://example.com/rawsource.ini


