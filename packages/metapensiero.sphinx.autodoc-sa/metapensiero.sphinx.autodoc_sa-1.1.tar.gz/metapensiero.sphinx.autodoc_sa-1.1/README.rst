.. -*- coding: utf-8 -*-
.. :Project:   metapensiero.sphinx.autodoc_sa -- Autodoc extension to pretty print canned SA queries
.. :Created:   Sat 14 Jan 2017 10:34:19 CET
.. :Author:    Lele Gaifax <lele@metapensiero.it>
.. :License:   GNU General Public License version 3 or later
.. :Copyright: © 2017 Lele Gaifax
..

================================
 metapensiero.sphinx.autodoc_sa
================================

Autodoc extension to pretty print canned SA queries
===================================================

 :author: Lele Gaifax
 :contact: lele@metapensiero.it
 :license: GNU General Public License version 3 or later

This is a very simple extension to Sphinx__ that injects the ability to recognize and pretty
print SQLAlchemy__ statements into its `automodule`__ and autoclass directives.

__ http://www.sphinx-doc.org/
__ http://www.sqlalchemy.org/
__ http://www.sphinx-doc.org/en/1.5.1/ext/autodoc.html?highlight=autoclass#directive-automodule


To use it, first of all you must register the extension within the Sphinx environment, adding
the full name of the package to the ``extensions`` list in the file ``conf.py``, for example::

  # Add any Sphinx extension module names here, as strings.
  extensions = ['metapensiero.sphinx.autodoc_sa']

Without further settings it uses the default SQLAlchemy `stringification strategy`__, but you
can explicitly choose the right *dialect* by setting ``autodoc_sa_dialect`` to a string
containing its fully qualified name, for example::

  autodoc_sa_dialect = 'sqlalchemy.dialects.postgresql.dialect'

Otherwise, you can set it using the ``-D`` option of the ``sphinx-build`` command, e.g. adding
``-D autodoc_sa_dialect=my.own.dialect`` to the ``SPHINXOPTS`` of the Makefile created by
``sphinx-quickstart``.

__ http://docs.sqlalchemy.org/en/rel_1_1/faq/sqlexpressions.html#how-do-i-render-sql-expressions-as-strings-possibly-with-bound-parameters-inlined

At this point, any documented SQLAlchemy core statement or ORM query, appearing either at the
module level or as a class attribute, will be *compiled* into SQL, beautified using
`sqlparse.format()`__ and added to the documentation wrapped within a ``code-block:: sql``
directive.

__ https://sqlparse.readthedocs.io/en/latest/api/#sqlparse.format
