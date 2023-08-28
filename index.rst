.. RelEng Docs documentation master file, created by
   sphinx-quickstart on Tue Nov 19 11:46:54 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=======================================
Welcome to RelEng Docs's documentation!
=======================================

Here is Mozilla's Release Engineering Group's more technical
documentation. You might also be interested in our `main web site`_.

.. _`main web site`: https://wiki.mozilla.org/Release

Contents:

.. toctree::
   :maxdepth: 4

   tutorials/index.rst
   how-to/index.rst
   reference/index.rst
   explanations/index.rst

.. toctree::
   :maxdepth: 4
   :caption: Overview and Procedures

   procedures/index.rst

.. toctree::
   :maxdepth: 4
   :caption: Documentation and Articles
   :glob:

   logs/index.rst
   architecture/index.rst
   best-practices/index.rst
   taskcluster/index.rst
   software.rst
   addons/index.rst
   Balrog & Updates <balrog/index.rst>
   Signing <signing/index.rst>
   releng_changelog
   future/index.rst
   machine-users.rst
   troubleshooting.rst

.. toctree::
   :caption: Meta
   :hidden:

   CODE_OF_CONDUCT
   Add a new repo to docs <adding_repo_to_releng_rtfd_account.rst>
   Add existing repo to docs <adding_docs_to_existing_code.rst>
   Maintaining this Documentation <README.md>
   tobewritten.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

* :ref:`tobewritten`

.. vim: nospell :
