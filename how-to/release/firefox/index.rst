.. _doing_a_release:

Firefox Release Process
=======================

Requirements and permissions to conduct a release
-------------------------------------------------

In order to initiate and ship a Firefox release, follow :ref:`these steps <release-duty-permissions>` to be granted the
various permissions required.

Specific steps required to initiate and release Firefox
-------------------------------------------------------

Once you have the permissions to conduct a release, the following is a walkthrough of how to do it.

High level
^^^^^^^^^^

1. Connect to Shipit.
2. Initiate a new release
3. Trigger the various phases of the release
4. Sign off in Balrog

Connect to the VPN
^^^^^^^^^^^^^^^^^^

Connect to the VPN. Visit `https://shipit.mozilla-releng.net/`. Sign in using your LDAP credentials.

Initiate a new release
^^^^^^^^^^^^^^^^^^^^^^

From Shipit, click on "New Release". Choose the target product, e.g. `Firefox Desktop`. Choose the target channel, e.g.
`Beta`, and select the desired revision you would like to ship from.

Revision - you must use a valid revision from the chosen channel. e.g. if you selected `Beta`, you must choose a
revision from `mozilla-beta <https://hg.mozilla.org/releases/mozilla-beta>`_.

Release ETA - If you are asked to give a "Release ETA", you do not need to fill this out.

Partials - partials should be auto populated. The list of partials are previous released versions that users are using
currently that we want to provide a special update to that is small in download size and is a diff of the user's current
version and the new version of Firefox you are about to create and ship. The auto-populated versions are usually based on
which versions are currently the most used by users.

A note on release promotion: Releases do not create new builds of Firefox. Instead, the automation will take existing
builds from the revision that was created and built when that revision was pushed (checked in). We refer to this as
"Release Promotion". For that reason, the revision must have builds started or complete and  associated with the target
revision. To see the builds of a given pushed revision, use `Treeherder <https://treeherder.mozilla.org>`_.

Version and build number - both of these are auto populated and can not be modified. The build number refers to how many
times we have had to create and recreate a release prior to shipping it to users. This often happens when the release
automation fails or or Firefox fails to pass QA.

Once the form is filled out, click `Start tracking it`. Note this does not actually kick off any release automation. It
merely primes the release in Shipit so that you can start triggering the various phases.

For more on how to create a release in Shipit, including UI screenshots, see `Relman's documentation <https://wiki.mozilla.org/Release_Management/Release_Process_Checklist_Documentation#Release_Tasks>`_

Trigger the phases of the release
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After creating a release in Shipit, you can see it via the "Releases" tab. From that tab, you can initiate a phase. For
most products, there are three phases: "promote", "push", and "ship".

Promote - as mentioned above, Shipit and release automation do not actually create any new Firefox builds. It instead
takes existing per-checkin builds from CI and signs, repacks, and publishes those to users. The promote phase consists
of release automation that does just that. Common tasks in this phase are signing, creating localization specific
builds, uploading build artifacts to a staging location on `http://archive.mozilla.org/` (S3), staging the release on
our update server, Balrog, and running install and update testing.

Push - This phase takes all the build artifacts that were promoted and uploaded to the staging location on archive.m.o
and pushes (copies) them to a final archive.m.o directory. It will also do some final update testing.

Ship - This final phase will make the release live and available on mozilla.org and start serving updates to existing
users via our update server Balrog.. See `Types of releases <#typesofreleases>`_ below for more.

In most cases, you would trigger each phase individually, one at a time. Note: by design, it is possible to only click a
later phase and Shipit is smart enough to backfill tasks from uninitiated earlier phases.

Once you trigger a phase, you can re-click on that phase to monitor the progress of the automation. This monitoring is
through the `Taskcluster's Task Monitor UI <https://firefox-ci-tc.services.mozilla.com/tasks/groups>`_. You have to keep
an eye on these tasks. If any of them fail, escalate it to the :ref:`Release Engineering team <release-duty-teams>` via
the proper :ref:`communications <release-duty-communication>`

For more on how to trigger phases of a release in Shipit, including UI screenshots, see `Relman's documentation <https://wiki.mozilla.org/Release_Management/Release_Process_Checklist_Documentation#Release_Tasks>`_

Signing off in Balrog
^^^^^^^^^^^^^^^^^^^^^

If the channel you are releasing is `Beta` or a mobile product, no further
action is required. If you are shipping a `ESR` or `Release` release, you also
need to sign off in Balrog itself via the `Balrog Admin UI <https://balrog.services.mozilla.com>`_

To guard against bad actors and compromised credentials we require that
any changes to primary release channels (beta, release, ESR) in Balrog
are signed off by at least two people.

After the scheduled change has been created by the “updates” task in the "ship"
phase that was triggered in Shipit, and prior to the desired release publish
time.

-  In context of the other rules, eg

   -  Firefox release:
      https://balrog.services.mozilla.com/rules?product=Firefox&channel=release&onlyScheduledChanges=1
   -  Firefox ESR:
      https://balrog.services.mozilla.com/rules?product=Firefox&channel=esr&onlyScheduledChanges=1

Further details and examples can be found on the [[Balrog page|Balrog
and Scheduled Changes]]

For more on how to sign off of a Balrog channel/rule change, including UI screenshots, see `Relman's documentation <https://wiki.mozilla.org/Release_Management/Release_Process_Checklist_Documentation#Release_Tasks>`_

How these taskcluster tasks are scheduled
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Shipit uses Taskcluster actions and the "taskgraph" tool to schedule what
tasks are needed in each phase. Taskcluster uses special release workers that are under Release Engineering control and
locked down to do the actual work. See `Source and under the hood <#Sourceandunderthehood>`_ below for more details.


Other Release Management Tasks
------------------------------

Release MGMT have a number of tasks and coordination items they need to address with each release. See an example of the `76 release checklist <https://docs.google.com/spreadsheets/d/1wRSzUShqVrg0O_5fa2Mr611R-DjhpcFk6swJvScj_mQ/edit#gid=221890705>`_

Escalating issues and communications
------------------------------------

For email, Slack, and Matrix communications with various release stakeholders, see the :ref:`communications <release-duty-communication>` section.

For troubleshooting a release automation issue, contact Release Engineering via above.

For any coordination or product specific issue, contact Release Management via above.


Source and under the hood
-------------------------

Taskcluster
^^^^^^^^^^^

Firefox is released via the same tooling that's used to build and test Firefox. We use our Mozilla in-house continuous
integration (CI) platform `Taskcluster <https://docs.taskcluster.net/docs>`_ to drive the tasks and workers. The main
service in this platform is the Taskcluster Queue. The queue takes requests of tasks and coordinates with a pool of
workers to actually conduct the task work. The various scheduling and dependency logic is defined in `taskgraph
<https://firefox-source-docs.mozilla.org/taskcluster/taskgraph.html>`_. The workers are trusted, locked down, and owned
by Release Engineering. They are `scriptworker <https://github.com/mozilla-releng/scriptworker>`_ based and the various
implementations live `here <https://github.com/mozilla-releng/scriptworker-scripts>`_

Signing
^^^^^^^

We use signing scriptworkers that interface with Mozilla's `autograph service
<https://github.com/mozilla-services/autograph>`_ 

Providing Updates
^^^^^^^^^^^^^^^^^

We use balrog scriptworkers that interface with Mozilla's `updater service, Balrog
<https://mozilla-balrog.readthedocs.io/en/latest/>`_ 

Shipit
^^^^^^

Shipit is used to initiate, track, and sign off on Firefox releases for each of the various stages. `Shipit
<https://github.com/mozilla-releng/shipit>`_ is a web app.

Off-Cycle Releases
------------------

.. toctree::
   :maxdepth: 1

   partner-repacks
   off-cycle-partner-repacks-and-funnelcake
