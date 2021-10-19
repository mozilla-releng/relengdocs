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
   :caption: Other Useful Documentation

   Balrog <https://mozilla-balrog.readthedocs.io/en/latest/index.html>
   Scriptworker <https://scriptworker.readthedocs.io/en/latest/index.html>
   Scriptworker Scripts <https://scriptworker-scripts.readthedocs.io/en/latest/index.html>
   Treeherder <https://treeherder.readthedocs.io/>
   Accessing CloudOps' Jenkins <https://github.com/mozilla-services/cloudops-deployment#accessing-jenkins>
   CloudOps Contact Info <https://mana.mozilla.org/wiki/display/SVCOPS/Contacting+Services+SRE>


.. toctree::
   :maxdepth: 4
   :caption: Overview and Procedures

   procedures/index.rst
   gecko_tests/new_config.rst


.. toctree::
   :maxdepth: 4
   :caption: Documentation and Articles
   :glob:

   logs/index.rst
   architecture/index.rst
   best-practices/index.rst
   taskcluster/index.rst
   hosts.rst
   software.rst
   addons/index.rst
   Balrog & Updates <balrog/index.rst>
   Signing <signing/index.rst>
   releng_changelog
   future/index.rst
   machine-users.rst
   troubleshooting.rst
   gecko_tests/index.rst

.. toctree::
   :caption: Meta
   :hidden:

   CODE_OF_CONDUCT
   Add a new repo to docs <adding_repo_to_releng_rtfd_account.rst>
   Add existing repo to docs <adding_docs_to_existing_code.rst>
   maintaining_these_docs.rst
   tobewritten.rst


Indices and tables
==================

* :ref:`Modifying these docs`

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

* :ref:`tobewritten`

.. vim: nospell :
