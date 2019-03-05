.. _Testing_Autograph:
.. index:: 
    single: Testing Autograph

Testing Autograph Stage
=======================

We currently use `Autograph`_ to sign our files with a number of our signing
formats. In CI, we point at autograph-prod, to avoid having autograph-stage
changes or availability affect production CI, nightlies, or releases.

However, sometimes the Autograph team needs to make changes to autograph-stage,
and want us to verify that it still works for us. Here's how.

.. _autograph-stage mar signing test:

Autograph-stage mar signing test
--------------------------------

There is a tier 3 task that doesn't run automatically. This task,
``mar-signing-autograph-stage-linux64-nightly/opt``, can be added to a push
that has run nightly builds and repackage tasks.

First, go to `mozilla-central treeherder`_. Make sure you're logged in
(top right).

Find the push with the most recent finished successful nightly. (It may be
easiest to search for ``nightly``).

On this push, click the down-arrow at the top right of the push. Choose
``Add new jobs``. The push will now show all the unscheduled jobs.

Find the autograph-stage mar-signing test job. It will be in the
``Linux x64 opt`` row, with the ``ms-stage(N)`` symbol. Click on it. It should
change colors to a dark grey.

Go back up to the top right of the push. Choose ``Trigger New Jobs``. Assuming
you've selected the right job, and you have the right scopes, it should now
create an ``add-new`` action task that triggers the autograph-stage mar-signing
task.

You can either watch treeherder or the taskcluster task. The task will be in
the on-push graph. The treeherder view may require you to enable ``tier 3``
in the ``Tiers`` menu at the top right of the page.

Once the ``mar-signing-autograph-stage-linux64-nightly/opt`` task goes green,
we know that autograph-stage has signed the mar, and signingscript has verified
that the signature matches the autograph-stage mar public key. Report back to
``#autograph`` on irc that it has passed.

.. _Autograph: https://mana.mozilla.org/wiki/display/SVCOPS/Autograph

Testing Autograph Prod
======================

Once we roll out to prod, we want to make sure it still works.

.. _autograph-prod mar signing test:

Autograph-prod mar signing test
-------------------------------

To test autograph-prod mar-signing, find a recent (but ideally not the
most-recent) nightly graph. Find a mar-signing task in that graph. To rerun it
via the `taskcluster-cli`_::

    # find the task id via treeherder
    #  - click on the task
    #  - find the taskId on the lower left
    tc-signin
    taskcluster task rerun -- <TASK_ID>

To rerun it via treeherder::

    - sign in to `mozilla-central treeherder`_ (top right of the page)
    - click on the task
    - find the ``...`` menu in the lower left of the page, click on it
    - choose ``Custom Action``
    - choose ``Rerun``
    - click ``Trigger`` in the lower right

Make sure this task runs green. If it goes green, then the task signed the
mar file(s) via autograph-prod, and verified the signature matches the
public key.

.. _taskcluster-cli: https://github.com/taskcluster/taskcluster-cli
.. _mozilla-central treeherder: https://treeherder.mozilla.org/#/jobs?repo=mozilla-central
