.. _taskcluster:

========================================
Taskcluster Administration and Debugging
========================================

Specifically for the FirefoxCI cluster.

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
    :maxdepth: 2
    :glob:

    uploading_an_image
    troubleshooting_workers
    taskcluster_cli
    rerun_vs_retrigger
    testing_relpro.md
    scopes
    known_problems
    ci_admin
    tc_staging
    how_tasks_are_triggered

.. vim: nospell :
