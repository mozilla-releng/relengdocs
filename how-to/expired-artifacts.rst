Recover from tasks with expired artifacts
=========================================

We sometimes have issues where a new Task or Task Graph depends on an older cached task whose key artifacts have expired. Recovering from this can be tricky, but the following steps should work for all cases:

1) Rebuild the cached tasks with the "Rebuild Cached Tasks" action. This should be done against the most recent revision in the affected repository. For example, if the problem is happening on mozilla-beta you can visit https://treeherder.mozilla.org/jobs?repo=mozilla-beta, click the carat in the top right corner, select "Custom Push Action", and then Trigger the ``rebuild-cached-tasks`` action in the modal that pops up.

2) Wait for the cached tasks to complete successfully. Until this has happened and the Taskcluster indexes have been updated, any new pushes or tasks created will potentially still use the old, broken cached tasks.

3) Push a new commit to the affected branch. (This is not strictly necessary in all cases, but doing so avoids any possibility that older cached tasks will be used, so it is recommended unless you are very certain about what you are doing.)

4) If you need tasks other than the ones created by the new push, create them now. For example, if your ultimate goal is to get a release shipped, it can now be scheduled.
