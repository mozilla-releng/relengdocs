.. _troubleshooting_workers:

Troubleshooting Workers
=======================

(This page needs fleshing out. Ideally we have a runbook where we can go from symptom to solution.)

Active workers
--------------

We can see recent worker activity in the `provisioners UI <https://firefox-ci-tc.services.mozilla.com/provisioners/>`__. For instance, if we're looking at ``gecko-3/b-linux``, we could go `here <https://firefox-ci-tc.services.mozilla.com/provisioners/gecko-3/worker-types/b-linux>`__. Click on the columns to change sorting order. Using the `task started <https://firefox-ci-tc.services.mozilla.com/provisioners/gecko-3/worker-types/b-linux?sortBy=Task%20Started&sortDirection=desc>`__ column can give you an idea of what spot instance workers are still around and running tasks.

Drilling down into the workers themselves, e.g. with `mac-v3-signing2 <https://firefox-ci-tc.services.mozilla.com/provisioners/scriptworker-prov-v1/worker-types/signing-mac-v1/workers/mdc1/mac-v3-signing2>`__, allows you to see the status of recent tasks that ran on that worker. This can give you a better idea if a single worker is busted, or if it's across the pool or multiple pools.

Worker Manager errors
---------------------

The `worker manager UI <https://firefox-ci-tc.services.mozilla.com/worker-manager>`__ lists the various pools. It shows current capacity and pending tasks, as well as links to view the workers and recent worker manager error messages, for each pool.

Drilling down into each workerType should show you the config. Generally this will be an expanded version of the `ci-configuration worker-pools config <https://hg.mozilla.org/ci/ci-configuration/file/tip/worker-pools.yml>`__.

Common types of error messages
------------------------------

``Instance Creation Error: Error calling AWS API: There is no Spot capacity available that matches your request.``

We get emails about this. This is also visible in the Worker Manager UI.

This means we've run out of spot instance capacity in a given region. A single instance of this is generally informative, not actionable. Many instances of this error message, combined with too many pending tasks and not enough capacity, may mean we need to adjust instance types or regions or the like.

``Instance Creation Error: Error calling AWS API: We currently do not have sufficient $INSTANCE_TYPE capacity in the Availability Zone you requested ($AVAILABILITY_ZONE). Our system will be working on provisioning additional capacity. You can currently get $INSTANCE_TYPE capacity by not specifying an Availability Zone in your request or choosing $ALTERNATE_AVAILABILITY_ZONES.``

We get emails about this. This is also visible in the Worker Manager UI.

This means this instanceType is not supported in this availability zone at all. We choose which availability zone to use randomly and retry on failure, so this is probably not fatal, but it can be noisy.

To stop getting this error message, we can mark a given instanceType family as invalid in a given availability zone `here <https://hg.mozilla.org/ci/ci-configuration/file/ba8263985ad932759ce36430f095f8ac952c93a4/environments.yml#l91>`__.

Quarantining workers
--------------------

Go to the worker view, e.g. `mac-v3-signing2 <https://firefox-ci-tc.services.mozilla.com/provisioners/scriptworker-prov-v1/worker-types/signing-mac-v1/workers/mdc1/mac-v3-signing2>`__. Make sure you're logged in (top right). Click on the three dots in the lower right hand corner. Choose a date to quarantine until (1000 years in the future is generally ok as long as we unquarantine hardware workers after they're ready to be put back into the pool), and quarantine it. The machine should stop taking tasks after the current task resolves.

Unquarantining workers
----------------------

Go to the worker view, e.g. `mac-v3-signing2 <https://firefox-ci-tc.services.mozilla.com/provisioners/scriptworker-prov-v1/worker-types/signing-mac-v1/workers/mdc1/mac-v3-signing2>`__. Make sure you're logged in (top right). Click on the three dots in the lower right hand corner and update the quarantine. Choose a date in the past and update the quarantine date. The worker should start claiming tasks within a minute or so if it's running and any tasks are pending.

Worker-manager slowness
-----------------------

See :ref:`worker_manager_issues`.

Viewing pending tasks
---------------------

You can modify `this query <https://sql.telemetry.mozilla.org/queries/78484/source>`__ to search for, say, ``windows10`` to determine why the number of pending has spiked by a thousand tasks.
