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

This will run every push to the ci-config repo; we only need to rerun if we want to update hooks or verify nothing has been changed manually since the last run.

You'll need :ref:`taskcluster_cli` for this.

.. code:: bash

   # Sign in via taskcluster cli
   eval $(taskcluster signin)

   # Apply changes to the staging taskcluster cluster
   ci-admin apply --environment staging 2>&1 | tee staging.out

Push to try
-----------
Until we fix the `firefox-ci hardcode <https://bugzilla.mozilla.org/show_bug.cgi?id=1765661>`__, We want to push `this patch <https://bugzilla.mozilla.org/attachment.cgi?id=9275932>`__ to try using ``./mach try release --migration central-to-beta -v 102.0b1`` or similar.

We can cancel the graph as soon as it gets scheduled; we only need the try push, not the production firefox-ci tasks. You'll need the try revision below.

Run fxci to send mozilla-central tasks to the staging cluster
-------------------------------------------------------------

.. code:: bash

   # Activate above virtualenv
   pyenv activate cienv

   # Set root url
   export TASKCLUSTER_ROOT_URL=https://stage.taskcluster.nonprod.cloudops.mozgcp.net

   # Log out in case we have previous tc creds
   unset TASKCLUSTER_CLIENT_ID; unset TASKCLUSTER_ACCESS_TOKEN

Run fxci
~~~~~~~~

.. code:: bash

   # Sign in via taskcluster cli
   eval $(taskcluster signin)

   # Set REVISION to the try commit
   REVISION=95f571f94f6d9c4e597d8a33fa27cf2fecf12f84

   # Run fxci
   fxci replay-hg-push try $REVISION

This will give you a URL like https://stage.taskcluster.nonprod.cloudops.mozgcp.net/tasks/J9WeztDYT4aQstuJUGOgIg . This is the `build-decision <https://hg.mozilla.org/ci/ci-configuration/file/tip/build-decision>`__ task URL, which will create a decision task.

Monitor the build-decision task
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once this goes green, the logs will link you to the decision task ID.

Watch the task group. Ideally whatever you're concerned about (in this case it was docker-worker artifact uploads) will go green.

Test the Github Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~

A `Github app`_ is connected to the Taskcluster staging instance and installed
on the `stage-taskcluster-test`_ repository. Run some tasks by creating a pull
request, verify that they are scheduled and show up in the Github checks
interface. Merge the pull request to create a `github-push` event and verify the
task is scheduled again.

.. note::

   This repo is not yet configured via `ci-configuration`, so you'll need to add scopes manually
   by `creating the appropriate roles in the web ui`_.

.. _Github app: https://github.com/apps/stage-taskcluster
.. _stage-taskcluster-test: https://github.com/mozilla-releng/stage-taskcluster-test
.. _creating the appropriate roles in the web ui: https://stage.taskcluster.nonprod.cloudops.mozgcp.net/auth/roles

Known issues
------------

Missing AMIs
~~~~~~~~~~~~

If you hit an error like ``Error calling AWS API: Not authorized for images: [ami-0fd21b9566eba5684]`` in `worker-manager <https://stage.taskcluster.nonprod.cloudops.mozgcp.net/worker-manager/infra%2Fbuild-decision/errors>`__, we probably need to share AMIs from the production FirefoxCI cluster to the staging cluster.

Pete was able to share them using `these steps <https://mozilla-hub.atlassian.net/browse/FCP-53?focusedCommentId=520218>`__. If we automate this, we may want to use the `ci-config ami list <https://hg.mozilla.org/ci/ci-configuration/file/tip/worker-images.yml>`__ instead. We may future this work, since we may be able to share the untrusted AMIs when recreating them, and we may not recreate them frequently before migrating to GCP.

Missing GCP workers
~~~~~~~~~~~~~~~~~~~

Relops should be able to share level 1 GCP worker images with the staging cluster.

Missing hardware workers
~~~~~~~~~~~~~~~~~~~~~~~~

This is expected. These tasks will hang and hit ``deadline-exceeded`` if you don't cancel them first.

Scriptworkers
~~~~~~~~~~~~~

We don't have scriptworkers pointed at the staging cluster, nor do we want to create those pools. That means that any scriptworker tasks will expire without being claimed, and downstreams won't run.

Secrets
~~~~~~~

`This script <https://hg.mozilla.org/build/braindump/file/a16d4c026782aafd47539d01ac900b38456a33f1/taskcluster/copy_secrets_to_staging.py>`__ populates a subset of [fake] secrets from fxci to staging, and `this script <https://hg.mozilla.org/build/braindump/file/a16d4c026782aafd47539d01ac900b38456a33f1/taskcluster/remove_secrets_from_staging.py>`__ removes them. We should only need to use these scripts if tasks die because they can't access staging secrets.
