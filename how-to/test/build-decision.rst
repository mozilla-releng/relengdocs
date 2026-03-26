Test Build Decision
===================

When updating ``build-decision``, it's a good idea to test your changes before
pushing them live. There are two approaches: a quick local dry-run against real
hg.mozilla.org, and a full end-to-end test using a Taskcluster hook.

Local dry-run
-------------

This validates the build-decision code path against real hg.mozilla.org without
deploying a Docker image. It exercises push info fetching, file list collection,
``.taskcluster.yml`` fetching, and task rendering — but does not submit a task.

1. Find a recent revision from mozilla-central::

     curl -sL 'https://hg.mozilla.org/mozilla-central/json-pushes?version=2&full=1&tipsonly=1'

2. Set the ``PULSE_MESSAGE`` environment variable with the revision::

     export PULSE_MESSAGE='{"payload": {"type": "changegroup.1", "data": {"pushlog_pushes": [{"pushid": 1}], "heads": ["<revision>"]}}}'

3. Run ``build-decision hg-push`` with ``--dry-run``::

     TASKCLUSTER_ROOT_URL=https://firefox-ci-tc.services.mozilla.com/ \
     uv run --package build-decision build-decision hg-push \
       --repo-url https://hg.mozilla.org/mozilla-central \
       --project mozilla-central \
       --level 3 \
       --repository-type hg \
       --trust-domain gecko \
       --dry-run

The rendered Decision task JSON will be logged. If you see ``Decision Task: {...}``
in the output, the test has passed.

Test with the hook
------------------

This tests the full Docker image end-to-end using the
`test-build-decision hook`_ in Taskcluster.

1. Push a PR to fxci-config. Wait for the ``docker-image-build-decision`` CI
   task to complete (visible in the GitHub checks UI).
2. Open the `test-build-decision hook`_ in Taskcluster web.
3. Edit the ``image`` field in the hook definition to reference the image built
   by the PR's ``docker-image-build-decision`` task::

     {
       "type": "task-image",
       "taskId": "<docker-image-task-id>",
       "path": "public/image.tar.zst"
     }

   Save the hook.
4. Fire the hook manually.

You should see a new event for the triggered hook. If it successfully creates a
Decision task, the test has passed!

.. _test-build-decision hook: https://firefox-ci-tc.services.mozilla.com/hooks/project-releng/cron-task-mozilla-releng-fxci-config%2Ftest-build-decision
