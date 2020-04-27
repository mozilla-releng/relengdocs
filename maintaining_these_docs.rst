.. _`Modifying these docs`:

==============================
Maintaining this Documentation
==============================

Overview
========

Release Engineering has a wide variety of documentation, served from
various locations. Per
`Releng RFC 0007 <https://github.com/mozilla-releng/releng-rfcs/blob/master/rfcs/0007-docs-location.md>`_,
we want to use this as a central location for Release Engineering documentation,
but will link to other locations from here when that makes sense.

We likely need to go through these docs and clean up.

Building the docs locally
-------------------------
#. Create a python virtualenv
#. ``pip install -r rtfd-requirements.txt``
#. ``make html`` will build the docs locally. Verify any changes by viewing ``_build/html/index.html``
#. Any new docs should be directly or indirectly linked to from ``index.rst``. (For example, if ``index.rst`` contains ``balrog/index.rst`` in its toctree, and the new doc is in the ``balrog/index.rst`` toctree, then the new doc is successfully indirectly linked.)
#. We support both markdown ``.md`` and reStructuredText ``.rst`` files. The former may be simpler to write and use; the latter have more powerful linking and nesting capabilities. See the `Sphinx docs <https://www.sphinx-doc.org/en/stable/>`_ for documentation.

Documenting Source Code
=======================

.. WARNING::
   old instructions; we may want to revisit!

We use Sphinx to generate our code documentation, and host it on Read the
Docs. There are two major phases to this:

    - :ref:`adding_docs_to_the_project`
    - :ref:`adding_repo_to_releng_rtfd_account`
