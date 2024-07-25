.. _taskcluster:

Administer Firefox-CI
=====================

These external docs are relevant to Mozilla's Firefox-CI Taskcluster instance:

- `Taskcluster docs`_
- :external+taskgraph:doc:`Taskgraph docs <index>`
- :external+firefox:doc:`Gecko in-tree taskcluster docs <taskcluster/index>`
- :external+scriptworker:doc:`Scriptworker docs <index>`
- :external+scriptworker-scripts:doc:`Scriptworker-scripts docs <index>`
- `Rotate CoT keys`_

.. _Taskcluster docs: https://firefox-ci-tc.services.mozilla.com/docs
.. _Rotate CoT keys: https://mana.mozilla.org/wiki/display/RelEng/Chain+of+Trust+key+rotation?flashId=459232040

.. toctree::
    :maxdepth: 1
    :caption: How-To Guides
    :glob:

    uploading_an_image
    troubleshooting_workers
    taskcluster_cli
    testing_relpro.md
    known_problems
    ci_admin
    fxci_upgrades
    tc_staging
    new_region
