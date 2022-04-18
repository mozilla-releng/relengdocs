.. _tc_staging:

Taskcluster Staging
===================

Mozilla has three Taskcluster clusters: firefoxci, staging, and
community. Release Engineering only deals with the first two; any
Releng-supported tasks need to run in the firefoxci cluster.

When to run these steps
-----------------------

Generally, the amount of testing we get in unit tests and the Staging, Community clusters is sufficient. We only really need to test FirefoxCI tasks in Staging for major Taskcluster version upgrades or other significant migrations or changes.

Setup
-----

1. clone
   `ci-configuration <https://hg.mozilla.org/ci/ci-configuration/>`__
   and make sure it’s up to date

   .. code:: bash

      # First time clone; if so, we can skip the other hg commands
      hg clone https://hg.mozilla.org/ci/ci-configuration/

      # Make sure we don't have local uncommitted changes
      hg status

      # Make sure we're not on a local committed change
      hg checkout -r 'last(public())'

      # Get latest commit
      hg pull -u

      # Compare revision against latest revision in https://hg.mozilla.org/ci/ci-configuration/
      hg log -r .

2. Set up a python virtualenv, install ci-admin and fxci

   .. code:: bash

      # Using pyenv and python >=3.7
      PYTHON_VERSION=3.8.0
      pyenv virtualenv $PYTHON_VERSION cienv
      pyenv activate cienv

      # Install ci-admin and fxci into the virtualenv;
      # these will follow the checked-out revision in the clone
      python setup.py develop

Log into TC Staging and run ci-admin
------------------------------------

.. code:: bash

   # Activate above virtualenv
   pyenv activate cienv

   # Set root url
   export TASKCLUSTER_ROOT_URL=https://stage.taskcluster.nonprod.cloudops.mozgcp.net

   # Log out in case we have previous tc creds
   unset TASKCLUSTER_CLIENT_ID; unset TASKCLUSTER_ACCESS_TOKEN

Diff
~~~~

.. code:: bash

   # Diff staging cluster's running config against ci-configuration on disk
   ci-admin diff --environment staging 2>&1 | tee staging.diff

Apply
~~~~~

You'll need :ref:`taskcluster_cli` for this.

.. code:: bash

   # Sign in via taskcluster cli
   eval $(taskcluster signin)

   # Apply changes to the staging taskcluster cluster
   ci-admin apply --environment staging 2>&1 | tee staging.out

Copy secrets to the Staging cluster
-----------------------------------

Some tasks in the m-c graph need secrets to run. I was able to get a set of secrets scopes from taskgraph, as of 2022-02-28::

    secrets:get:gecko/gfx-github-sync/token
    secrets:get:project/engwf/gecko/3/tokens
    secrets:get:project/perftest/gecko/level-3/perftest-login
    secrets:get:project/releng/gecko/build/level-3/*
    secrets:get:project/releng/gecko/build/level-3/conditioned-profiles
    secrets:get:project/releng/gecko/build/level-3/conditioned-profiles
    secrets:get:project/releng/gecko/build/level-3/gecko-docs-upload
    secrets:get:project/releng/gecko/build/level-3/gecko-generated-sources-upload
    secrets:get:project/releng/gecko/build/level-3/gecko-symbol-upload
    secrets:get:project/taskcluster/gecko/hgfingerprint
    secrets:get:project/taskcluster/gecko/hgmointernal

It's possible we just need the ``gecko/build`` and ``taskcluster/gecko/hg*`` secrets.

`This script <https://hg.mozilla.org/build/braindump/file/tip/taskcluster/copy_secrets_to_staging.py>`__ copies that subset of secrets from fxci to staging. We need to do the following to use it:

- set the ``NOOP`` boolean to ``False`` in the script

Run fxci to send mozilla-central tasks to the staging cluster
-------------------------------------------------------------

.. code:: bash

   # Activate above virtualenv
   pyenv activate cienv

   # Set root url
   export TASKCLUSTER_ROOT_URL=https://stage.taskcluster.nonprod.cloudops.mozgcp.net

   # Log out in case we have previous tc creds
   unset TASKCLUSTER_CLIENT_ID; unset TASKCLUSTER_ACCESS_TOKEN

Find a commit
~~~~~~~~~~~~~

Go to `Treeherder <https://treeherder.mozilla.org/jobs?repo=mozilla-central>`__ or the `pushlog <https://hg.mozilla.org/mozilla-central/pushloghtml>`__ to find the latest commit. This commit will need to be the latest commit in a given, non-``DONTBUILD`` push.

.. image:: staging/treeherder1.png

In the above treeherder screenshot, ``dde3e56805b9`` is the latest revision on the latest push, but is ``DONTBUILD``, resulting in zero tasks running other than the decision task. ``23f9ff7daa01`` is the tip revision of the latest push without ``DONTBUILD``. Clicking the ``copy`` button next to it will copy the long SHA to your clipboard.

.. image:: staging/pushlog1.png

Similarly, in the above pushlog screenshot, you can see the same information, with long revision SHAs.

Run fxci
~~~~~~~~

.. code:: bash

   # Sign in via taskcluster cli
   eval $(taskcluster signin)

   # Set REVISION to the above commit you found
   REVISION=23f9ff7daa01b1273edb9c1df04436d895983b58

   # Run fxci
   fxci replay-hg-push mozilla-central $REVISION

This will give you a URL like https://stage.taskcluster.nonprod.cloudops.mozgcp.net/tasks/PHY82PPMQmOz_qYucrSHOw . This is the `build-decision <https://hg.mozilla.org/ci/ci-configuration/file/tip/build-decision>`__ task URL, which will create a decision task.

Monitor the build-decision task
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once this goes green, the logs will link you to the decision task ID.

Watch the task group. Ideally whatever you're concerned about (in this case it was docker-worker artifact uploads) will go green.

Known issues
------------

Missing AMIs
~~~~~~~~~~~~

If you hit an error like ``Error calling AWS API: Not authorized for images: [ami-0fd21b9566eba5684]`` in `worker-manager <https://stage.taskcluster.nonprod.cloudops.mozgcp.net/worker-manager/infra%2Fbuild-decision/errors>`__, we probably need to share AMIs from the production FirefoxCI cluster to the staging cluster.

Pete was able to share them using `these steps <https://mozilla-hub.atlassian.net/browse/FCP-53?focusedCommentId=520218>`__. If we automate this, we may want to use the `ci-config ami list <https://hg.mozilla.org/ci/ci-configuration/file/tip/worker-images.yml>`__ instead. We may future this work, since we may be able to share these AMIs when recreating them, and we may not recreate them frequently before migrating to GCP.

Scriptworkers
~~~~~~~~~~~~~

We don't have scriptworkers pointed at the staging cluster, nor do we want to create those pools. That means that any scriptworker tasks will expire without being claimed, and downstreams won't run.
