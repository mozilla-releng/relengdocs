Perform Release Duty
====================

More detailed information on specific ReleaseDuty topics:

.. toctree::
    :maxdepth: 1
    :glob:

    desktop/*
    scheduled-deploys
    merge-duty/*
    interrupt-duty

ReleaseDuty is a role within the Release Engineering team. It is conducted on a rolling rotation matching one person
against one release cycle (currently 4 weeks). Below you will find a description of the expectations and resources
needed to do the role.

Expectations
------------

If you're reading this, it means you're ramping up as an official ReleaseDuty squirrel within Mozilla RelEng, so please
allow us to give you a warm welcome!

The role mainly involves handling all the coordination and communication with other teams as well as doing
all the operational tasks to make sure the release workflow is as smooth as possible.

While this role can get quite disruptive, we prefer this approach of assigning the responsibility to a small set of
people who will own all the tasks, while we shield the others in Release Engineering from interruptions.

Being ReleaseDuty means a couple of things:
 * Communication and coordination with other teams
 * Handle all incoming releases
 * Fix and debug any potential errors in the automation
 * Develop and improve the Release Automation process and tools

.. _release-duty-communication:

Communication
-------------

Slack Channels
~~~~~~~~~~~~~~~

Join Mozilla's Slack network using information from `the wiki <https://wiki.mozilla.org/NDA-Slack>`__

You ought to be present and pay attention to conversations happening in:

* **#releaseduty-mobile** (where `mobile` and other Github releng-backedup automation projects's teams raise issues)
* **#releng-notifications** (where automation notifications are going, useful to know the state of our automation infrastructure state)
* **#taskcluster-cloudops** (where CloudOps double-checks with RelEng whether it's safe to deploy changes or not on their side)

Optionally, you may want to monitor these channels also:

* **#incidents**
* **#release-coordination**

Matrix Channels
~~~~~~~~~~~~~~~

Join Mozilla's Matrix network using information from `the wiki <https://wiki.mozilla.org/Matrix>`__

You ought to be present and pay attention to conversations happening in:

* **#sheriffs:mozilla.org** (where CIDuty team helps with various hiccups that infra might encounter))
* **#releaseduty:mozilla.org** (main RelEng dedicated communication channel for releaseduty)
* **#firefox-ci:mozilla.org**
* **#tbdrivers:mozilla.org** (This is the Thunderbird release drivers Matrix channel. **@rjl:mozilla.org** (Rob) should be able to invite you)

Relduty Notifications
~~~~~~~~~~~~~~~~~~~~~

For the duration of ReleaseDuty, you must also add ``relduty`` as a highlighted
word in both Slack and Matrix.

For Slack, go to ``Preferences -> Notifications``, then add ``relduty`` under
the ``My keywords`` section.

For Matrix, go to ``Settings -> Notifications``, then under ``Mentions &
Keywords`` type ``relduty`` in the text box and press the ``Add`` button.

You may remove both keywords once your ReleaseDuty rotation is finished.

Email
~~~~~

Please join the following groups to stay on top of the communication regarding the releases:

 * All types of sign-offs and approvals should go to `release signoff mailing list <https://groups.google.com/a/mozilla.org/g/release-signoff/>`__
 * All discussion topics should go to `release drivers mailing list <https://groups.google.com/a/mozilla.org/g/release-drivers>`__
 * `RelEng internal mailing list <release@mozilla.com>`__
 * `Thunderbird release drivers mailing list <https://groups.google.com/a/mozilla.org/g/thunderbird-drivers>`__ - Click "contact owners and managers" and request permission

Meetings and Calendars
~~~~~~~~~~~~~~~~~~~~~~

See the `Release owners <https://wiki.mozilla.org/Release_Management/Release_owners>`__ list to determine who is ReleaseDuty for each release.

Regular meetings are a vital part of making sure all the teams are kept informed and consulted during the release
process, although ReleaseDuty does not routinely attend these meetings. To view those meetings in your calendar you need to subscribe to the following calendar:

 * `Releases Scheduling <https://calendar.google.com/calendar/embed?src=mozilla.com_dbq84anr9i8tcnmhabatstv5co@group.calendar.google.com>`__ (You can add it following RelMan's `docs <https://wiki.mozilla.org/Release_Management#Calendar_Updating>`__) – If their instructions don't work, try to the “Add to Google Calendar” button at the `web version of the calendar <https://calendar.google.com/calendar/embed?src=mozilla.com_dbq84anr9i8tcnmhabatstv5co@group.calendar.google.com>`__.

**If you join a calendar and it's blank, you may need to delete it and get a calendar invitation from an existing subscriber**

.. _release-duty-permissions:

Permissions
-----------

Several tools for managing releases are protected or private. In order to do your job, you need to be granted access to
a bare minimum:

 * Access to the `VPN <https://mana.mozilla.org/wiki/display/SD/VPN>`__
 * A `Bugzilla <https://bugzilla.mozilla.org/>`__ account
 * Read/Write access to `Balrog <https://balrog.services.mozilla.com/>`__
 * Read/Write access to `Ship-it v2 <https://shipit.mozilla-releng.net/>`__

How to get VPN access
~~~~~~~~~~~~~~~~~~~~~

First you need to be connected to the Mozilla VPN. See the `mana page <https://mana.mozilla.org/wiki/display/SD/VPN>`__
for how to get set up and started with connecting to the VPN.


How to get Ship-it access
~~~~~~~~~~~~~~~~~~~~~~~~~

You need to be added to the `vpn_cloudops_shipit` LDAP group. File an `Infrastructure & Operations` bug under the `Infrastructure: LDAP
<https://bugzilla.mozilla.org/enter_bug.cgi?format=__default__&cloned_bug_id=1773239&product=Infrastructure%20%26%20Operations&component=Infrastructure%3A%20LDAP>`__
component requesting to be granted shipit access.

Replace the email in the Summary field and have someone in Release Engineering vouch for you in the bug.


How to get Balrog access
~~~~~~~~~~~~~~~~~~~~~~~~

Similar to Shipit, you need to be added to the `balrog` and `vpn_balrog` LDAP groups and have someone add you as a user
and attach you to the `releng` role through the Balrog admin UI.

For VPN group access, file a ticket with IT similar to `this one <https://bugzilla.mozilla.org/enter_bug.cgi?format=__default__&cloned_bug_id=1773241&product=Infrastructure%20%26%20Operations&component=Infrastructure%3A%20LDAP>`_.
Have someone in Release Engineering vouch for you in the bug.

Then, ask a Release Engineer to be added to the Balrog admin user list and attached to the `releng` role.


Tooling for debugging and rerunning tasks
-----------------------------------------

Note many of the task-related operations can be conducted through Treeherder such as rerunning/retriggering a task.
There is also a command line tool that can be used instead of the UI.

taskcluster
~~~~~~~~~~~

Release tasks are usually run through `Taskcluster <https://docs.taskcluster.net/>`__, which has a useful `Command-line
interface <https://github.com/taskcluster/taskcluster/tree/main/clients/client-shell#readme>`__

To get started with the CLI:

  * Download the appropriate binary for your OS (Mac or Linux)
  * Copy the binary somewhere useful, such as somewhere in your `$PATH <http://www.linfo.org/path_env_var.html>`_ such as ``/usr/local/bin/taskcluster``
  * Make it executable ``chmod a+x /path/to/taskcluster``
  * Export the root URL ``export TASKCLUSTER_ROOT_URL='https://firefox-ci-tc.services.mozilla.com/'`` 
  * Run ``taskcluster signin``  to open a browser window and allow you to get temporary client credentials. By default this is valid for 24 hours. **The command will display two** ``export`` **commands you must copy/paste into your shell**
  * Familiarize yourself with the subcommands, starting with ``taskcluster help``


in-bulk taskcluster operations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes operations need to be performed against a bulk of tasks. In
order to do that, RelEng has developed a handful of scripts to ease the
operations. They lie around in the ``braindump`` repository.

::

   hg clone https://hg.mozilla.org/build/braindump/
   cd braindump/taskcluster
   mkvirtualenv workspace
   pip install taskcluster

Follow `this resource <https://github.com/taskcluster/taskcluster/tree/main/clients/client-shell#installation>`__ to download the ``taskcluster-cli`` tool or read
the previous section.

Once ``taskcluster-cli`` is installed, ensure right env vars are set,
login and operate the tasks.

::

   export TASKCLUSTER_ROOT_URL='https://firefox-ci-tc.services.mozilla.com/'
   eval taskcluster signin
   python tc-filter.py --graph-id <group-task-id> --state failed --action rerun

To speed things up even more, one can add this to ``~/.zshrc`` (or your shell's rc file) for an alias
to reduce the scopes and time-limit of the signin:

::

   tc-relduty=$'eval `TASKCLUSTER_ROOT_URL=https://firefox-ci-tc.services.mozilla.com/ taskcluster signin --expires 1h -s "queue:rerun-task:*\nqueue:cancel-task:*"`'


graph inspection
~~~~~~~~~~~~~~~~
Inspecting a task group from the UI can sometimes be heavy for the browser. Instead, one can use a script to watch the graph progress locally via poll & sleep. In the same braindump
aforementioned directory, there is a graph-progress script that can be run like:

::

   bash graph-progress.sh <TASK-GROUP-ID>


Firefox bookmarks
~~~~~~~~~~~~~~~~~

These bookmarklets should help you view tasks and taskgroups in Firefox.

 * Go to Bookmarks -> Manage Bookmarks
 * Gear symbol -> Add Bookmark
 * Add the following bookmarks:
  
 | Name: ``task inspector``
 | Location: ``https://firefox-ci-tc.services.mozilla.com/tasks/%s``
 | Keyword: ``task``
 
 | Name: ``taskgroup inspector``
 | Location: ``https://firefox-ci-tc.services.mozilla.com/groups/%s``
 | Keyword: ``taskgroup``

 | Name: ``stop``
 | Location: ``javascript:stop();``

 * ``stop`` can be used to stop further loading in the Task Group Inspector. It shouldn't be used when actively monitoring (i.e.: watching for failures), but it can greatly speed things up if you're using it for other reasons. Be sure to wait for the initial tasks to load before you use it.

Now if you go to your URL bar, you can type ``task TASKID`` or ``taskgroup TASKGROUPID`` and you'll go to that task or
taskgroup in the inspector.

After ReleaseDuty
-----------------

After your tour of ReleaseDuty, in the past it was customary to fix any documentation
or automation issues discovered.  Now make sure you file any bugs so issues can be included
in a future sprint or work cycle.

Ensure the next duty cycle have signed up to any phabricator reviews, such as the periodic file updates reviews.

Miscellaneous
-------------

 * Bugzilla issues regarding specific releases/WNP are filed under `Release Engineering:Release Requests <https://bugzilla.mozilla.org/enter_bug.cgi?format=__default__&product=Release%20Engineering&component=Release%20Requests>`__
 * Issues regarding automation are filed under `Release Engineering:Release Automation <https://bugzilla.mozilla.org/enter_bug.cgi?product=Release%20Engineering&component=Release%20Automation>`__

.. _release-duty-teams:

Hand Off
--------

If a scheduled release has not completed its graphs prior releaseduty signing
off, an explicit hand-off describing release state should be sent to
individual folks in releng that are scheduled to come online next or will be
around for a while after you. #releaseduty in Matrix is best. A release@m.c email
would be useful too.

Escalation
----------

If a release is blocked. The normal flow is to:

1. confirm issue
2. determine what service, task kind, infrastructure, or external
   dependency is involved
3. file a ticket
4. determine which team(s) and person(s) should be escalated.

   a. Searching the People Directory is useful for org and ownership charts.
   b. bugzilla and github history
   c. source code history

5. escalate in the appropriate Slack and Matrix channel(s). 
   At a minimum, `#releaseduty in Matrix <https://matrix.to/#/#releaseduty:mozilla.org>`__
6. determine who is available to help based on above. What hours they
   work, who is their manager, etc
7. ask for help if you can’t determine the above.

Good resources within releng:
 * general release configuration (taskgraph): aki
 * scopes / ciadmin: mtabara
 * chainoftrust (cot): aki
 * scriptworker (general): aki
 * beetmoverscript / bouncer / artifact related: mtabara/aki
 * signing / signingscript / autograph: aki
 * balrog / balrogscript / updates related: bhearsum/mtabara
 * l10n / treescript / addonscript: aki/mtabara
 * pushapkscript / mozapkpublisher: mtabara
 * shipit / shipitscript: bhearsum

Other useful resources
----------------------

*  More on `Release Management <https://wiki.mozilla.org/Release_Management>`__

Glossary
--------

*  WNP - The “What's New Page” can be set to appear after an upgrade, to tell end-users of any changes in the browser they should be aware of.
*  FF - Firefox
*  TB - Thunderbird
*  b1, b2, etc - beta release 1, beta release 2, etc

FAQ ---

1. *What does release-promotion refer to?*

'Release promotion' is simply the idea that we take an already existing CI build from (e.g. beta) and promote that to
being the build we release/ship to users. Prior to this approach, we had always rebuilt Firefox at the start of each new
release. Long story short, release promotion entails taking an existing set of builds that have already been triggered
and passed QA and “promoting” them to be used as a release candidate. More on promotion can be found on our docs `here
<https://firefox-source-docs.mozilla.org/taskcluster/release-promotion.html#in-depth-relpro-guide>`__

2. *What is the train model?*

Since 2012 Mozilla moved to a fixed-schedule release model, otherwise known as the Train Model, in which we released
Firefox every six weeks to get features and updates to users faster and move at the speed of the Web. In 2020 Mozilla
switched to releasing every four weeks, hence, every four
weeks the following merges take place: `mozilla-beta <http://hg.mozilla.org/releases/mozilla-beta/>`__ =>
`mozilla-release <http://hg.mozilla.org/releases/mozilla-release/>`__ `mozilla-central
<http://hg.mozilla.org/mozilla-central/>`__ => `mozilla-beta <http://hg.mozilla.org/releases/mozilla-beta/>`__
 
*Also:* `whattrainisitnow.com <https://whattrainisitnow.com/>`__

We used to have an intermediate branch named 'aurora' in between central and beta but that was brought to end-of-life
during April-May 2017.  Instead, early beta releases are branded as 'DevEdition'.

3. *What is a partner repack change for FF?*

Partner repacks refer to 3rd party customized branded versions of Firefox that Mozilla is taking care of for some of its
clients. With some exceptions, most of the partner reconfigs lie under private repositories. Mostly, the partner repacks
don't need too much of RelEng interference as all bits are held under private git repos and are directly handled by the
partnering companies

4. *Is there calendar-based release scheduled for Thunderbird as for Firefox?*

No. It's irregular. Conversations happen on #tbdrivers and TB mailing list and they trigger their release in Ship-it.

5. *Why don't I see update_verify_beta for dot releases?*

From time to time, a handful of issues precipitate a dot release. When that happens, its behavior slightly varies from a
normal release. A normal release (e.g. 43.0, 44.0, etc) has its RC shipped to beta channel first before making it to the
release channel - for testing purposes, update verify steps are taking place both ways, hence update_verify_release and
update_verify_beta steps. Upon a successful testing phase we ship the RC on the beta channel and then on the release
channel, following which we merge the code for the next release cycle so that the beta release bumps its version. In the
lights of this logic, a dot release (e.g. 43.0.1 or 44.0.1) happens a certain amount of time after the official release.
For that reason, a dot release can't be tested in beta channel as the at-that-moment beta version is greater than the
dot release version, hence the updater would refuse to downgrade. Therefore, there is only one cycle of update_verify
for dot releases (update_verify_release == update_verify in this case).

6. *Is there explicit signoff from RelMan for DevEdition builds?*

No, after b1, there isn't signoff from RelMan on DevEdition builds. QA only verifies the DevEdition builds every two
weeks. With the exception of b1, and assuming all the tasks complete as expected, the DevEdition builds should be
shipped at the same time as we receive signoff for the corresponding desktop builds.

7. *How do I coordinate with marketing on release day?*

Join the **#release-coordination** channel on Mozilla Slack

8. *What is cdntest and localtest?*

``-cdntest`` and ``-localtest`` channels serve releases from the releases
directory (mirrors or CDN) or candidates directory depending on the release and
channel. They are testing channels used before we serve from the *real* update
channel, but they use the *actual files* that will be served once a release is
published.

9. *What's the difference between Firefox and DevEdition?*

In the beta cycle, ``Firefox`` and ``Devedition`` are different products
built based on the same in-tree revision. Their functionality is the
same but branding options differ.

10. *What do the terms ``releases directory``, ``mirrors`` and ``CDN`` mean?*

``releases directory``, ``mirrors`` and ``CDN`` are different terms for the same
concept - the CDN from which shipped releases are served.

11. *What does* ``watershed`` *mean?*

``watershed`` refers to a situation when we release a new version of a product
(Firefox 57), but users on an older version (Firefox 53) are not able to update.
This is a ``watershed`` and we would need to ensure we don't serve invalid updates.
