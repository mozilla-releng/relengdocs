FirefoxCI cluster upgrades
==========================

As of H1 2022, the Taskcluster, Cloudops, and Releng teams have committed to rolling out upgrades to the FirefoxCI cluster at a regular cadence.

Process
-------

We now have a regular cadence of scheduled upgrades, as noted in the `Public - FirefoxCI Cluster Taskcluster Upgrades calendar`_.

Several days before:

- Determine which upgrades and/or maintenance procedures are needed. Ideally we have baked the target Taskcluster version in the Staging and Community, and tested any changes that might negatively affect the FirefoxCI cluster.

- If there are any changes that are in question, ideally the knowledgeable developers are ready to respond during/after the upgrade, and/or we have a rollback plan in place.

- We track JIRA tickets at the `Deploying to FirefoxCI mana page <https://mana.mozilla.org/wiki/pages/viewpage.action?spaceKey=TAS&title=Deploying+to+FirefoxCI>`__.

- We remind everyone about these upgrades by sending out emails like `this <https://groups.google.com/a/mozilla.org/g/dev-platform/c/UGCNchYxVns>`__, and checking with `Relman <https://wiki.mozilla.org/Release_Management/Release_owners>`__ before the upgrade to make sure there are no releases in-flight.

.. _minor_tc_upgrade:

Minor version upgrade process
-----------------------------

As of 2022.04.13, we have been successful rolling out minor version Taskcluster upgrades *without a tree closure*. We also managed to upgrade the database instance RAM during such a non-tree-closure window, which made the DB unavailable for ~10-15min. This only resulted in ~2 failed tasks, which went green on rerun. So if we want to roll out a minor version upgrade or other short-term outage maintenance tasks:

- Send an email noting that this is a tree-closure-less upgrade several days before (Releaseduty)
- Check with Relman before proceeding (Releaseduty)
- Roll out the maintenance fixes and cluster upgrades (Cloudops team)
- Check on smoketests (Taskcluster team)
- Check treeherder and ask Sheriffs if there are any broken tasks (Releaseduty)
- Send an email saying the upgrade is finished (Releaseduty)
- Update the `changelog`_.

.. _major_tc_upgrade:

Major version upgrade process
-----------------------------

If there is a major version upgrade, or other maintenance/migration that will have larger side effects than a few busted tasks in a half hour of maintenance, let's follow these steps:

- Identify the potential issues we might hit post-upgrade/maintenance/migration
- :ref:`Test in taskcluster staging <tc_staging>`
- Create a rollback + testing plan
- Send an email noting that this is a tree-closure upgrade several days before, update the `Public - FirefoxCI Cluster Taskcluster Upgrades calendar`_ (Releaseduty).
- Close trees 2+hours before (Sheriffs or Releaseduty)
- Check with Relman before proceeding (Releaseduty)
- Roll out the maintenance fixes and cluster upgrades (Cloudops team)
- Check on smoketests (Taskcluster team)
- Check treeherder and ask Sheriffs if there are any broken tasks (Releaseduty)
- Reopen trees (Sheriffs or Releaseduty)
- Send an email saying the upgrade is finished (Releaseduty)
- Update the `changelog`_.

.. _Public - FirefoxCI Cluster Taskcluster Upgrades calendar: https://calendar.google.com/calendar/u/0?cid=Y19mbWQ3YmZwZ3IzOTI5cnJtaWVqYmszdXM2OEBncm91cC5jYWxlbmRhci5nb29nbGUuY29t
.. _changelog: https://github.com/mozilla/build-relengdocs/blob/main/releng_changelog.md
