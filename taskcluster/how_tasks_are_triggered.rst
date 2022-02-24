.. _how_tasks_are_triggered:

How Tasks are Triggered
=======================

How are tasks triggered in Taskcluster?

- You can create arbitrary tasks through, e.g. `the create task API/UI <https://firefox-ci-tc.services.mozilla.com/tasks/create>`__.
- Or you can encode one or more tasks in `.taskcluster.yml <https://github.com/mozilla-releng/scriptworker/blob/8d35c98f58f0fb54367da854560721beb53f8f18/.taskcluster.yml>`__
- If you pass a certain threshold of complexity, you probably want your ``.taskcluster.yml`` to schedule a decision task, which will create a task graph via `taskcluster-taskgraph <https://taskcluster-taskgraph.readthedocs.io/en/latest/>`__.

... But what generates the task(s) in ``.taskcluster.yml``?

[Pulse ->] hooks -> build-decision
----------------------------------

We have a python module named `build-decision`_ that knows how to trigger decision tasks for hg.m.o pushes and github+hg.m.o cron tasks. This is bundled in the `build-decision docker image <https://hg.mozilla.org/ci/ci-configuration/file/tip/taskcluster/docker/build-decision>`__.

Once we build that image in `automation <https://treeherder.mozilla.org/jobs?repo=taskgraph>`__, Releng chooses a given build-decision image to use and uploads it to `docker-hub <https://hub.docker.com/repository/docker/mozillareleases/build-decision>`__. We then update the pinned image in the `hg push hook template <https://hg.mozilla.org/ci/ci-configuration/file/388e286a59bf134e053dd55264572dc9e36e2640/hg-push-template.yml#l35>`__ and the `cron hook template <https://hg.mozilla.org/ci/ci-configuration/file/388e286a59bf134e053dd55264572dc9e36e2640/cron-task-template.yml#l35>`__; the next time we run :ref:`ci-admin <ci-admin>`, ci-admin updates the various on-push (`e.g. <https://firefox-ci-tc.services.mozilla.com/hooks/hg-push/mozilla-central>`__) and cron (`e.g. <https://firefox-ci-tc.services.mozilla.com/hooks/project-releng/cron-task-mozilla-central>`__) hooks.

hg.m.o on-push
~~~~~~~~~~~~~~

When we push a change to hg.m.o, we send a `pulse message <https://mozilla-version-control-tools.readthedocs.io/en/latest/hgmo/notifications.html?highlight=pulse#pulse-notifications>`__. The `mozilla-central hg-push hook <https://firefox-ci-tc.services.mozilla.com/hooks/hg-push/mozilla-central>`__ listens to ``exchange/hgpushes/v2 with mozilla-central``, creates a task using the build-decision image, and sets the ``PULSE_MESSAGE`` env var to the contents of the pulse message. This task then creates the decision task, which in turn creates a task graph as appropriate.

We can replicate this later, using `fxci <https://hg.mozilla.org/ci/ci-configuration/file/tip/src/fxci>`__, via the ``fxci replay-hg-push`` subcommand.

Cron
~~~~

We have three types of cron hooks:

Time-based cron hooks
^^^^^^^^^^^^^^^^^^^^^

When we enable either `gecko-cron <https://hg.mozilla.org/ci/ci-configuration/file/388e286a59bf134e053dd55264572dc9e36e2640/projects.yml#l27>`__ (firefox desktop or thunderbird only), or `taskgraph-cron <https://hg.mozilla.org/ci/ci-configuration/file/388e286a59bf134e053dd55264572dc9e36e2640/projects.yml#l46>`__ for a project, and when there is a `.cron.yml <https://hg.mozilla.org/mozilla-central/file/d0676cb0864b870062fed21bc900d6fbb3cf5670/.cron.yml>`__ at the top of the repository, then we create a cron task `every 15 minutes <https://hg.mozilla.org/ci/ci-configuration/file/388e286a59bf134e053dd55264572dc9e36e2640/build-decision/src/build_decision/cron/schema.yml#l68>`__ to see if anything should run. This cron task runs `build-decision`_, which knows how to generate a cron decision task.

For example, the `mozilla-central cron hook <https://firefox-ci-tc.services.mozilla.com/hooks/project-releng/cron-task-mozilla-central>`__ has a schedule of ``0 0,15,30,45 * * * *``, and runs the ``cron`` command entry point in the ``build-decision`` docker image.

Manually triggered cron hooks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes we want to be able to trigger some of these cron tasks outside of the regularly scheduled times. (Sometimes we even have 0 regularly scheduled times for specific cron tasks, and we only trigger them manually.)

To enable this, we specify the ``project.cron.targets``, like for mozilla-central `here <https://hg.mozilla.org/ci/ci-configuration/file/388e286a59bf134e053dd55264572dc9e36e2640/projects.yml#l209>`__; in ``cron.targets`` we enable the desktop nightlies to be triggered off-cycle, as well as l10n-bumper and others. The ``scriptworker-canary`` cron hook accepts input (``allow-input: true``).

So when we run :ref:`ci-admin <ci-admin>`, we generate things like the `mozilla-central l10n-bumper cron hook <https://firefox-ci-tc.services.mozilla.com/hooks/project-releng/cron-task-mozilla-central%2Fl10n-bumper>`__, which has no schedule, and we have the ``'--force-run=l10n-bumper'`` option specified in the ``cron`` command. We can trigger these hooks manually.

The `mozilla-central scriptworker-canary cron hook <https://firefox-ci-tc.services.mozilla.com/hooks/project-releng/cron-task-mozilla-central%2Fscriptworker-canary>`__ similarly has no schedule, and has the ``'--force-run=scriptworker-canary'`` option. Because we allow for input, we set the ``HOOK_PAYLOAD`` env var to the payload that we send to the hook.

Pulse-triggered cron hooks
^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes we want to be able to trigger some of these cron hooks via some external, non-time-based, non-manually-triggered signal. In this case, we can add a pulse binding to a given cron hook.

In the `android-l10n-tooling project <https://hg.mozilla.org/ci/ci-configuration/file/388e286a59bf134e053dd55264572dc9e36e2640/projects.yml#l868>`__, we have the ``update-l10n`` cron.target where we specify ``bindings`` as follows::

    - exchange: exchange/taskcluster-github/v1/push
      routing_key_pattern: primary.mozilla-mobile.fenix
    - exchange: exchange/taskcluster-github/v1/push
      routing_key_pattern: primary.mozilla-mobile.android-components
    - exchange: exchange/taskcluster-github/v1/push
      routing_key_pattern: primary.mozilla-mobile.firefox-tv
    - exchange: exchange/taskcluster-github/v1/push
      routing_key_pattern: primary.mozilla-lockwise.lockwise-android

And indeed, the `update-l10n hook <https://firefox-ci-tc.services.mozilla.com/hooks/project-releng/cron-task-mozilla-l10n-android-l10n-tooling%2Fupdate-l10n>`__ generated by :ref:`ci-admin <ci-admin>` has no schedule; it does have those pulse bindings, it includes the ``cron`` option ``'--force-run=update-l10n'``, and is also manually triggerable.

The github push pulse event appears to be `sent by taskcluster-github <https://github.com/taskcluster/taskcluster/blob/5a25a717299e9eae61d7ed0935ceb028b8319a26/services/github/src/exchanges.js#L90-L105>`__, so we trigger this hook whenever there is a github push to these repos, but we can also trigger the hook manually if there's an issue with the pulse-driven pipeline.

Through action hooks
--------------------

As noted in :ref:`actions_tc_yml`, we embed the contents of .taskcluster.yml into action hooks, which are named by .tc.yml hash. This avoids having an intermediate task::

    hook -> action task -> result

rather than::

    hook -> build-decision -> action task -> result

Some of the rationale and debate are surfaced in `bug 1463522 <https://bugzilla.mozilla.org/show_bug.cgi?id=1463522>`__ and `bug 1415868 comment 77 <https://bugzilla.mozilla.org/show_bug.cgi?id=1415868#c77>`__. We may want to revisit this debate, but until then, our action hooks directly create an action task.

However, these are different than other hooks, in that action tasks are run against a previously-run decision task, and rely on the decision task's artifacts, especially ``actions.json``.

Through taskcluster-github
--------------------------

Taskcluster-github `listens to Github events, directly parses .taskcluster.yml, and creates decision tasks <https://github.com/taskcluster/taskcluster/blob/7888f56b64c86be4b36efb6b8d2ca4c21143c2d4/services/github/src/handlers.js#L658-L661>`__.

We may want to revisit whether we want the app to do this, or if we want an intermediate `build-decision`_ task in between.

.. _`build-decision`: https://hg.mozilla.org/ci/ci-configuration/file/tip/build-decision
