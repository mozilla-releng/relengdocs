.. _taskcluster:

Administer Firefox-CI
=====================

These external docs are relevant to Mozilla's Firefox-CI Taskcluster instance:

- `Taskcluster docs`_
- `Taskgraph docs`_
- `Gecko in-tree taskcluster docs`_
- `Scriptworker docs`_
- `Scriptworker-scripts docs`_
- `Rotate CoT keys`_

.. _Taskcluster docs: https://firefox-ci-tc.services.mozilla.com/docs
.. _Taskgraph docs: https://taskcluster-taskgraph.readthedocs.io/en/latest/
.. _Gecko in-tree taskcluster docs: https://firefox-source-docs.mozilla.org/taskcluster/taskcluster/index.html
.. _Scriptworker docs: https://scriptworker.readthedocs.io/en/latest/
.. _Scriptworker-scripts docs: https://scriptworker-scripts.readthedocs.io/en/latest/
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
