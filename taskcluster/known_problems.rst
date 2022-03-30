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

.. _missing mercurial features:

Missing Mercurial features when Cloning the Repo
------------------------------------------------

Symptoms
~~~~~~~~

After updating the version of Mercurial used on newer branches, tasks on older
branches might start failing with errors like:

.. parsed-literal::
   abort: repository requires features unknown to this Mercurial: revlog-compression-zstd!

This happens because repos cloned via newer versions of Mercurial are often
incompatible with older versions of Mercurial. Since workers have a shared
checkout cache between tasks, if a worker first claims a task on e.g,
`mozilla-central`, clones the repo, and then claims a task on
`mozilla-release`, the latter task might fail if it is using an older
Mercurial.

Solution
~~~~~~~~

The solution is to increment the cache identifier associated with the checkout
cache. For example, the Gecko decision tasks use `this cache name`_. Changing
the name (e.g incrementing `v2` -> `v3`), will ensure workers don't re-use the
same cache across disparate branches.

The downside to doing this is that tasks on older branches with less traffic
will have more cache misses, resulting in longer runtimes which could impact
our ability to ship expediently. To mitigate this, consider backporting the
image bump that caused the Mercurial upgrade to beta, release and esr branches.

.. _this cache name: https://searchfox.org/mozilla-central/rev/1ca8ea11406642df4a2c6f81f21d683817af568d/.taskcluster.yml#217

.. _worker_manager_issues:

Workers are spinning up slowly
------------------------------

First, see :ref:`troubleshooting_workers`.

Second, as of 2022.01.26, we have had a number of issues with worker-manager. There is a single process that goes through worker pool by worker pool to spin workers up and down on demand. The Azure workers, in particular, take a long time to spin up and down, and these processes block spinning other pools up or down. There's not much we can do here except adjust our idle times, which isn't the ideal solution. Otherwise we wait for the Taskcluster team to fix the issues::

1. `Bug 1736329 - gecko-3/decision workers not taking tasks <https://bugzilla.mozilla.org/show_bug.cgi?id=1736329>`__
2. `Bug 1735411 - windows 2004 test worker backlog (gecko-t/win10-64-2004) <https://bugzilla.mozilla.org/show_bug.cgi?id=1735411>`__
3. `Bug 1741946 - Investigate the best way to go about the Windows 10 Azure worker delays <https://bugzilla.mozilla.org/show_bug.cgi?id=1741946>`__
4. RFC issue `UI to visualize and reprioritize scheduled+pending tasks <https://github.com/taskcluster/taskcluster-rfcs/issues/172>`__
5. RFC issue `Revisit worker idle time shutdown <https://github.com/taskcluster/taskcluster-rfcs/issues/170>`__
6. (marked as dup) `Investigate running multiple worker-managers <https://github.com/taskcluster/taskcluster/issues/5064>`__
7. `worker-manager: Timeout leads to stuck process <https://github.com/taskcluster/taskcluster/issues/5003>`__
8. `worker-manager: Azure workers register when state != REQUESTED <https://github.com/taskcluster/taskcluster/issues/4999>`__
9. `Combine worker-manager provisioner and worker scanner in to a single processes <https://github.com/taskcluster/taskcluster/issues/4987>`__
10. `Provide worker counts and capacity by state for worker pools <https://github.com/taskcluster/taskcluster/issues/4942>`__
11. `limited concurrency for worker scanning <https://github.com/taskcluster/taskcluster/issues/4810>`__
12. `Measure and improve performance of the worker query in provisioning loop <https://github.com/taskcluster/taskcluster/issues/3163>`__

.. _ci-configuration: https://hg.mozilla.org/ci/ci-configuration/
