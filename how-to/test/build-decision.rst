Test Build Decision
===================

When updating the build-decision image, it's a good idea to run a quick test
before pushing it live. First :ref:`build and publish <build-decision-image>` a
new ``build-decision`` image. Once your image is on Docker hub:

1. Open the `cron-task-ci-ci-configuration/test-build-decision`_ hook in
   Taskcluster web.
2. Edit the ``image`` field in the hook definition to point to your recently
   uploaded image. Save the hook.
3. Fire the hook manually.

You should see a new event for the triggered hook. If it successfully creates a
Decision task, the test has passed!

.. _cron-task-ci-ci-configuration/test-build-decision: https://firefox-ci-tc.services.mozilla.com/hooks/project-releng/cron-task-ci-ci-configuration%2Ftest-build-decision
