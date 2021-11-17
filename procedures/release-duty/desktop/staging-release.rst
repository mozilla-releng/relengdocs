.. _staging-release:

We have a number of tasks that _only_ run on Betas, Releases, and ESRs. Because of this, these tasks are at high risk of failure when we uplift a new Gecko version to `mozilla-beta`. Many scriptworkers fall into this category, but certain verification jobs, like update verify, are also notably included.

When making changes to tasks like this staging releases are the most effective way to ensure that your changes are correct, and haven't regressed anything.

Run staging releases
~~~~~~~~~~~~~~~~~~~~

Permissions
^^^^^^^^^^^

To do a staging release, you need to be able to push to try, access to the Mozilla VPN, and have staging shipit read/write access.

See the :ref:`production documentation for how to get Shipit and VPN access <release-duty-permissions>`.

How-To
^^^^^^

In order to prepare a smooth ``b1`` and ``RC``, staging releases should
be run weekly or at least one week before RC week. In order for this to
happen, we're using `staging releases submitted to
try <https://firefox-source-docs.mozilla.org/tools/try/selectors/release.html>`__.

**For central to beta migration**

-  hop on ``central`` repository
-  make sure you're up to date with the tip of the repo
-  ``mach try release --version <future-version.0b1> --migration central-to-beta --tasks release-sim``

**For beta to release migration**

-  hop on ``beta`` repository
-  make sure you're up to date with the tip of the repo
-  ``mach try release --version <future-version.0> --migration beta-to-release --tasks release-sim``

.. note:: Get ``future-version`` from `shipit-staging <https://shipit.staging.mozilla-releng.net/>`__. Ie.: If the version in shipit is ``94.0b14`` use ``94.0b15``

These will create try pushes that look-alike the repos once they are
merged. Once the decision tasks of the newly created CI graphs are
green, staging releases can be created off of them via the
`shipit-staging <https://shipit.staging.mozilla-releng.net/>`__
instance. For how to create a release via Shipit, refer to the
:ref:`production documentation <doing_a_release>`. The same applies to staging,
just ensure you are using the staging instance
(https://shipit.staging.mozilla-releng.net).

One caveat here is the list of partials that needs to be filled-in.
:warning: The partials need to exist in Ship It dev, Balrog stage, as well as the _production_ archive.mozilla.org server. There's a `helper script in the braindump repository <https://hg.mozilla.org/build/braindump/file/tip/releases-related/just-give-me-partials.sh>` that will help you find previous releases that meet this criteria.

Once the staging releases are being triggered, it's highly recommended
that at least a comment is being dropped to Sheriffs team
(e.g. ``Aryx``) to let them know these are happening in order to: \*
avoid stepping on each others toes as they may run staging releases as
well \* make sure we're up-to-date to recent patches that they may be
aware of

:warning:
   Allow yourself enough time to wait for these staging releases
   to be completed. Since they are running in ``try``, they have the lowest
   priority even on the staging workers so it usually takes longer for them
   to complete.

Staging scriptworkers
^^^^^^^^^^^^^^^^^^^^^

**Reusing builds from a recent release**

Outside of mergeduty, during development cycles, we often need to work around a single specific scriptworker, whether
that entails changing the in-tree code or the ``*script`` itself. While
triggering staging releases is a valid solution, it is often an
expensive one as it generates an entire graph. In order to be more
efficient, one can use the `scriptworker selector`_ which aims to run a
selection of scriptworker tasks against builds from a recent release. There are a number of
preset groups of tasks to run. The list is configured `here`_ and it get be extended for
other tasks/products. To get the list of task sets, along with the list of tasks they will run:

::

   mach try scriptworker list

The selector defaults to using tasks from the most recent beta.To use
tasks from a different release, pass ``--release-type <release-type>``:

::

   mach try scriptworker --release-type release linux-signing

**Override workertype**

One can extend the aforementioned behavior by overriding the
worker type to use. This is particularly useful for staging releases
against the DEV scriptworker environment. Most of the workerType configs
we have in-tree are configured as ``level-{1,3}`` for fake/production and ``level-1-dev``
for dev.

But the latter is not present in-tree by default so it needs to be
amended. More information on this can be found in the
`scriptworker-scripts documentation`_. One can either manually change
the intree kind's config to that specific worker-type, or can simply pass an
argument to aforementioned command to make the replacement,
e.g. ``mach try scriptworker TASK-TYPE --release-type beta --worker-override <alias>=<suffix>``,
where ``TASK-TYPE`` is chosen from one of the
``mach try scriptworker list`` returns and ``alias`` comes from the
taskcluster ci config `file`_). For example, running the beetmover jobs against the most recent beta
release, but on the DEV worker-type:

::

   mach try scriptworker beetmover-candidates --release-type beta --worker-override beetmover=gecko-1-beetmover-dev

.. _scriptworker selector: https://firefox-source-docs.mozilla.org/tools/try/selectors/scriptworker.html?highlight=scriptworker
.. _here: https://hg.mozilla.org/mozilla-central/file/tip/tools/tryselect/selectors/scriptworker.py#l18
.. _scriptworker-scripts documentation: https://scriptworker-scripts.readthedocs.io/en/latest/scriptworkers-dev.html
.. _file: https://hg.mozilla.org/mozilla-central/file/tip/taskcluster/ci/config.yml#l437


