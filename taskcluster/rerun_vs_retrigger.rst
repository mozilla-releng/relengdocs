Rerun vs Retrigger
==================

We have the capability to both ``rerun`` a task and to ``retrigger`` it.

In the case of a ``rerun``, we take a ``failed`` or ``exception`` task
and increment the ``runId``; the task is requeued to run immediately
without checking dependency statuses; it can potentially go green the
next run.

In the case of a ``rerun`` with ``--force``, we can take a successfully
completed task, increment its ``runId``, and requeue it to run
immediately without checking dependency statuses. **This can completely
hork release graphs’ Chain of Trust verifiability; proceed with
caution.**

In the case of a ``retrigger``, we take a ``failed`` or ``exception``
non-release task, copy its task definition, change its ``taskId`` and
timestamps, and schedule one or more brand new tasks that are largely
copies of the original task.

In the case of a ``retrigger (disabled)``, we can take a release task
and create a copy to run. This is generally the wrong thing to do if
we’re trying to unblock a broken release graph, and generally the right
thing to do if we’re trying to verify a new scriptworker pool deployment
is good.

Here are some scenarios when one is preferable to another, as of October
2021:

Intermittent tests in treeherder: retrigger
-------------------------------------------

Because ``retrigger`` allows us to schedule ``n`` copies of a given
task, and because tests don’t need to pass Chain of Trust (CoT)
verification from downstream tasks, a ``retrigger`` of intermittent
tasks can allow us to run many copies of a single test concurrently.

Broken Pull Request tasks: rerun
--------------------------------

If a Github Pull Request requires that a test goes green before you can
merge, a ``rerun`` of an intermittent failed task will potentially mark
that test as green if it passes the next run.

Broken release tasks: rerun
---------------------------

If a release task is broken for intermittent or external dependency
reasons, we should ``rerun`` to unblock the rest of the graph. A
``retrigger`` will spawn new tasks but leave the busted task in place. A
``retrigger`` that spawns downstreams will fork the entire graph, which
could get extremely messy and break Chain of Trust verification. For
this reason, we have explicitly marked ``retrigger`` as ``(disabled)``
on release tasks; we can still ``force`` these through if desired, but
in general we don’t want to.

Testing scriptworker pools outside of the release: retrigger (force)
--------------------------------------------------------------------

If we deployed a new production scriptworker pool, and if, as is best
practice, our scriptworker tasks are idempotent, we can
``retrigger (force)`` a previously green release or nightly task.

For instance, if we deployed a new signingscript production pool, we can
find a nightly graph from a couple days ago, and
``retrigger (disabled)`` a nightly signing task, with ``force: true``,
through action hooks. Because the new task is a) idempotent, b)
CoT-verifiable, and c) doesn’t pollute the output of the previously-run
signing task, we get a new signing task run that leaves the previous
nightly graph CoT-verifiable.

(This is as opposed to ``rerun (force)`` of a nightly or release signing
task. The SHAs of the artifacts of that ``taskId`` will change and no
longer match the SHAs of the artifacts used in downstream tasks; this is
discouraged and could force a build 2 if we do so in an in-flight
release graph.)

Notarization poller timeouts: rerun (force)
-------------------------------------------

For Apple Notarization, sometimes we have to use a ``rerun (force)``:

-  ``notarization-part-1`` submits the build to Apple’s Notarization
   service correctly
-  ``notarization-poller`` polls Apple, but that times out.

We have the capability of letting the notarization poller run for 10+
hours until the notarization service is finally ready, but in many
cases, simply resubmitting the build will result in a faster turnaround.
In this case, ``rerun (force)`` the ``notarization-part-1`` task, then
``rerun`` the poller task once the part 1 task finishes.

Release tasks with broken dependencies: cancel + rerun
------------------------------------------------------

If a release task fails repeatably, but for some reason shouldn’t
actually block the release (the bustage is somehow expected, and none of
the artifacts are used by downstream tasks), it’s possible to let the
dependent tasks run anyway with a ``cancel`` followed by ``rerun``,
after making sure all other dependencies completed successfully.

Deadline-exceeded leaf node release tasks
-----------------------------------------

If a release task has failed and passed its (generally 1 day) deadline,
and it’s a leaf node (e.g., not in the middle of a complex release
graph) and we still want to run it, we can force retrigger via actions.

.. Important::

   The previous broken task will remain, so the graph will remain in
   a failed or exception state. If the task has downstreams that rely
   on their output, this can result in a huge mess, and we’re better
   off either going with a build 2 or resorting to
   :ref:`advanced-relpro-usage`. Only use this approach for leaf nodes
   that don't have downstream dependent tasks that depend on artifacts
   from the current task, once they've passed their deadline.

-  Go to the task in the taskcluster UI
-  Make sure you’re logged in, top right
-  Click the three dots in the lower right
-  ``Retrigger (disabled)`` and set the ``force`` flag to ``true``.
   Click on the ``Retrigger (disabled)`` link in the lower right.

This will create an action task that creates a copy of this
deadline-exceeded release task, but with a new ``taskId`` and updated
timestamps.

We would do this if we want the result of the leaf release task. For
example, if we want a ``mark-as-shipped`` task to run to mark the
release as shipped in shipit, or a version bump, or similar.
