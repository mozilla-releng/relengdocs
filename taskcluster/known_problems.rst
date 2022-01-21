.. _known_problems:

Known Problems
==============

This page contains some known issues with the FirefoxCI cluster, what they're
symptoms are and how to resolve them.

.. _actions_tc_yml:

Actions are broken after modifying ``.taskcluster.yml``
-------------------------------------------------------

Anytime someone modifies ``.taskcluster.yml``, the hooks need to be
re-generated since they depend on the hash of this file.

Symptoms
~~~~~~~~

Action tasks will fail to run. Sheriffs will likely be the first to notice this
and will close the trees due to retriggers and backfills not working.

Solution
~~~~~~~~

Re-run ``ci-admin``. The easiest way is to land a change to the `ci-configuration`_
repo, though it can also be done manually (see :ref:`ci-admin`). Upon
deployment complete in Jenkins (see #releng-notifications), actions will be working
again.

History
~~~~~~~

We wanted to avoid action hooks having an intermediary task, a la::

    hook ->
    intermediary task clones repo, triggers hook task through .taskcluster.yml ->
    hook task runs the desired action

Instead, we went with::

    hash-named hook with .taskcluster.yml baked in ->
    hook task runs the desired action

This means that whenever .taskcluster.yml changes, we need to rebuild the hooks.

Missing Scopes after Branch Rename
----------------------------------

Some repos have specific scopes associated with a named branch, so e.g if we're
changing ``master -> main``, there may be failures.

Symptoms
~~~~~~~~

Tasks start failing due to scopes errors.

Solution
~~~~~~~~

Scan the `ci-configuration`_ repo for your project and see if we were granting
any special scopes to the old branch. If so, update the name to the new
branch and land.


.. _ci-configuration: https://hg.mozilla.org/ci/ci-configuration/
