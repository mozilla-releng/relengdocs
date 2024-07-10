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

Re-run ``ci-admin``. The easiest way is to land a change to the `fxci-config`_
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

Scan the `fxci-config`_ repo for your project and see if we were granting
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

Second, as of 2022.01.26, we have had a number of issues with worker-manager. There is a single process that goes through worker pool by worker pool to spin workers up and down on demand. The Azure workers, in particular, take a long time to spin up and down, and these processes block spinning other pools up or down. There's not much we can do here except adjust our idle times, which isn't the ideal solution. Otherwise we wait for the Taskcluster team to fix the issues:

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

.. _fxci-config: https://github.com/mozilla-releng/fxci-config

.. _workers not spawning:

Workers Not Spawning After Image Bustage
----------------------------------------

If there's a problem in a worker image, worker-manager may not spawn any new
workers even after the issue is fixed. This happens because the workers with
the problematic image are still running, even though they are unable to claim
tasks. However, worker-manager doesn't know this, so won't spawn any new
workers until the broken ones expire or are terminated.

These problematic workers *won't* show up in the Taskcluster Web UI, as the
queue service is unaware of workers until they claim a task.

Symptoms
~~~~~~~~

Backlogs will persist even after fixing a worker image. This will be most
noticeable on pools with a low max capacity (like Decision pools), as they are
more likely to get entirely filled with broken workers (in which cases no
further tasks would run).

Solution
~~~~~~~~

Run this script in braindump to automatically scan for and terminate these
broken workers:
https://hg.mozilla.org/build/braindump/file/tip/taskcluster/terminate_broken_workers.py

.. _push-msix fails:

push(MSIX) fails: "push to Store aborted: pending submission found"
-------------------------------------------------------------------

pushmsixscript pushes Firefox to the Microsoft Store. The Store rejects
any new submission if there is a pending submission (one which has been
uploaded but not yet released). Release Management has asked that
pushmsixscript not delete pending submissions, in case that pending submission
was created manually.

Symptoms
~~~~~~~~
The push(MSIX) task fails with Exception status. The task log shows
"push to Store aborted: pending submission found" and "ERROR - There is
a pending submission for this application on the Microsoft Store. Wait
for the pending submission to complete, or delete the pending submission.
Then retry this task."

Solution
~~~~~~~~
Delete the pending submission from the Store manually; Release Management
has access. Once the pending submission has been deleted, re-run the
failed push(MSIX) task.

.. _push-msix fails without explanation:

push(MSIX) starts failing, or reports "Request it is not IngestionWeb or IngestionApi"
--------------------------------------------------------------------------------------

pushmsixscript pushes Firefox to the Microsoft Store; some push failures are caused by Store outages or changes to the Store API.

Symptoms
~~~~~~~~
In general, if pushmsixscript suddenly starts failing, without any recent changes, the problem may be a change to the Store. Several such incidents have reported an error message "Request it is not IngestionWeb or IngestionApi". These errors tend to be permanent and only resolve after complaining to Microsoft.

Solution
~~~~~~~~
Report the incident to the mozilla-microsoft-discuss mailing list, https://groups.google.com/a/mozilla.com/g/mozilla-microsoft-discuss. Also consider opening an issue on https://github.com/microsoft/StoreBroker.
https://github.com/mozilla-releng/scriptworker-scripts/issues/923 documents one
such incident.
