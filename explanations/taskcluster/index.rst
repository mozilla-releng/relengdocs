Firefox-CI & Taskcluster
========================

`Taskcluster`_ is Mozilla's home grown task execution framework and CI service.
Mozilla runs two instances of Taskcluster; `Community`_ and `Firefox-CI`_.

The ``community`` instance is operated by the Taskcluster team. It acts as a
reference instance and primarily provides CI for projects that are adjacent to,
but not strictly owned by MoCo.

The ``firefox-ci`` instance is operated by Release Engineering. It provides CI
for most MoCo products (including Firefox) and supporting repos.

This section goes into some detail on core Taskcluster concepts, as well as
Firefox-CI specific extensions that underpin Mozilla's CI.

.. toctree::
   :maxdepth: 2

   how_tasks_are_triggered
   scopes
   rerun_vs_retrigger

.. _Taskcluster: https://taskcluster.net/
.. _Community: https://community-tc.services.mozilla.com/
.. _Firefox-CI: https://firefox-ci-tc.services.mozilla.com/
