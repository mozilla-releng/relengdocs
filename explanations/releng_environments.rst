Releng Test Environments
========================

When Releng needs to test something, we can use a testing environment to do so.

Environment Models
------------------

One model for doing so is creating monolithic development, integration, staging, and production environments, where everything is duplicated to keep testing self-contained. For Mozilla, that might include multiple duplicates of the following services:

  - HG + git VCS servers
  - Pulse
  - Taskcluster cluster
  - Autograph
  - Treeherder
  - Bugzilla
  - Balrog
  - archive.m.o
  - www.mozilla.com
  - Shipit
  - Bouncer

This model allows us to test anything and everything, knowing that we are fully self-contained and cannot affect other environments.

However, all services would need to stay in a known state, or our testing might hit corner case issues that would never happen in production. Duplicating all services, even those that we're not directly testing, could be expensive, in terms of both money and effort. It can be hard to keep everything in sync, especially across team boundaries. It can also be hard to redeploy everything simultaneously, and finding the differences between environments when an issue crops up in one environment but not another can be time-consuming.

Because of these issues, we have gone with a different model: being able to spin up test environments for specific services, often testing them against production in a read-only or limited/level-1 fashion. A common theme: an outage in any of the below environments should not affect production, including Continuous Integration (if we point at, say, Staging Autograph for signing on Autoland, and that service goes down or the Autograph team decides to test experimental and potentially broken code or configurations on Staging Autograph, then Autoland will be negatively affected by a staging environment. This is wrong; use a dep signer on production Autograph instead.)

Service Environments
--------------------

Taskcluster Stage
~~~~~~~~~~~~~~~~~
https://stage.taskcluster.nonprod.cloudops.mozgcp.net/

Only for testing Taskcluster changes, generally before a major Taskcluster release rollout to the FirefoxCI cluster (see :ref:`major_tc_upgrade`). The Taskcluster team has also historically used this as a development/integration/staging cluster for the Community cluster.

Balrog Stage
~~~~~~~~~~~~
https://balrog-admin-static-stage.stage.mozaws.net/

Primarily for testing balrog changes, but we also submit staging Firefox Desktop releases to this service as well.

(Because staging Firefox Desktop releases are written to Balrog Stage but staging Firefox Desktop Update Verify, partials, etc. need to reference previous release builds (and we have very few complete, fully successful staging Firefox Desktop releases in Balrog Stage + staging archive) we have a mishmash of pointing at read-only production and read-write staging. We could improve this by syncing production to staging more regularly/fully, and/or running end-to-end staging releases more often + to completion, and/or having a clever way to fall back to production for read-only release information for certain cases, e.g. partials and update verify.)

Staging Archive
~~~~~~~~~~~~~~~
https://bucketlister-delivery.stage.mozaws.net/pub/ , but this will change with GCS.

Primarily for testing beetmover changes, but we also submit staging Firefox desktop releases to this set of buckets as well. Similar to Balrog Stage, the difference between which releases are populated on prod and stage Archive make it difficult to do staging release Partials and Update Verify and the like easily and cleanly.

Autograph Stage
~~~~~~~~~~~~~~~
https://autograph-external.stage.autograph.services.mozaws.net

Only for testing Autograph changes, so we should have *zero* signingscript or iscript signing formats that target Autograph Stage, except for any formats that are explicitly for testing Autograph Stage functionality (see :ref:`Testing_Autograph`).

Staging Shipit
~~~~~~~~~~~~~~
https://shipit.staging.mozilla-releng.net/

Primarily for testing shipit changes, but we also generally submit staging releases through this service as well (see :ref:`staging-release`)

Stores
~~~~~~
We have no staging environments for stores, e.g. Google Play, the Microsoft Store, Flathub, Docker Hub. This means we're limited in how much testing we can do outside of production: oftentimes our non-production scriptworker pools for these stores merely do spot checks on the artifacts or task definition, without actually uploading any files anywhere.

Scriptworker Environments
-------------------------
(Also see `cert levels <https://firefox-source-docs.mozilla.org/taskcluster/signing.html#cert-levels>`_ and `signing scriptworker workerTypes <https://firefox-source-docs.mozilla.org/taskcluster/signing.html#signing-scriptworker-workertypes>`_.)

We have 3 categories of scriptworker environments:

Production
~~~~~~~~~~

As in ``release`` or ``level 3``. These scriptworker pools contain secrets used to sign and ship software to users, and should be locked down security-wise. These need to be up and working at all times so we can ship chemspills.

Depend / non-prod
~~~~~~~~~~~~~~~~~
The ``dep`` pools, a.k.a. ``depend`` or ``non-prod``, ``level 1`` or ``level-t`` (see `Why do all other scriptworkers have level-1 and level-3 but signing has level-t and level-3 <https://scriptworker-scripts.readthedocs.io/en/latest/scriptworkers-FAQ.html?highlight=level#why-do-all-other-scriptworkers-have-level-1-and-level-3-but-signing-has-level-t-and-level-3>`_) can be, in fact, production pools in terms of availability. This is especially true for the ``level-t`` dep signing scriptworkers, since we sign with these on Autoland and other trees on-push. The CI pipeline will stop if these pools are not available. However, their secrets are self-signed or throwaway. Non-shipping secrets, so they are non-production in terms of the release pipeline.

With the other, non-signing dep pools, if they're down, they may not close Autoland and other trees, but they're used for staging releases in PRs and on Try, by Releng and Sheriffs and developers. Because of this, we should keep these pools in working order and not test arbitrary code on them.

Dev
~~~
These are the Releng playground for testing arbitrary changes. These are shared pools for the entire team, so best practice is to ask around to make sure no one is using a given dev pool before pushing changes (and keeping a copy of your changes elsewhere, in case someone force-pushes to your dev branch).

Staging Releases
----------------
See :ref:`staging-release`.

As mentioned above, we use Staging Balrog, Staging Archive, Staging Shipit as needed. These are based off of staging Github repos, Github pull requests, or the Try repo.

Tasks like update verify and partials that require a history of previous releases tend to be fragile, since we don't have a full set of releases in Staging Shipit, Balrog, and Archive, and tend to test using a combination of read-only production and read-write staging. Ideally we would have a more robust story here, but we haven't been able to prioritize this above solving other, more outward-facing and frequent issues.
