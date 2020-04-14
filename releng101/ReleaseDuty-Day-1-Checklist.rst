Release Duty Day 1 Checklist
============================

If you're reading this page it means that you're ramping up as an
official releaseduty squirrel within Mozilla RelEng, so please allow us
to give you a warm welcome!

Releaseduty is a designated pass-the-token role that we assign every 6
weeks to members of the team. The role mainly involves handling all the
coordination and communication with other `teams <#teams>`__ as well as
doing all the operational tasks to make sure the release workflow is as
smooth as possible.

While this role can get quite disruptive, we prefer this approach of
assigning the responsibility to a small set of people who will own all
the tasks, while we shield the others in Release Engineering from
interruptions.

Being ReleaseDuty means a couple of things: - Communication and
coordination with other teams - Handle all incoming releases - Fix and
debug any potential errors in the automation - Develop and improve the
Release Automation process and tools

Communication
-------------

Most of the steps and milestones of a release will be sent by email. The
rest of the communication takes place in a few IRC channels.

The automation status is sent by email, and very spammy.

Meetings are usually conducted using
`Vidyo <https://mana.mozilla.org/wiki/display/SD/Vidyo>`__

Matrix Channels
~~~~~~~~~~~~~~~

Join Mozilla's Matrix network using information from `the wiki <https://wiki.mozilla.org/Matrix>`__

You ought to be present and pay attention to conversations happening in:

-  **#sheriffs:mozilla.org** (where CIDuty team helps with various hiccups that infra
   might encounter))
-  **#releaseduty:mozilla.org** (main RelEng dedicated communication channel for
   releaseduty)
-  **#firefox-ci:mozilla.org**

Email
~~~~~

As ReleaseDuty you need to *subscribe* to certain mailing lists.

-  All types of sign-offs and approvals should go to `release signoff
   mailing list <https://mail.mozilla.org/listinfo/release-signoff>`__
-  All releng automation emails should go to
   `release-automation-notifications <https://groups.google.com/a/mozilla.com/forum/?hl=en#!forum/release-automation-notifications>`__
-  All discussion topics should go to `release drivers mailing
   list <https://mail.mozilla.org/listinfo/release-drivers>`__

These other mailing lists will likely have useful discussions and
information: - `RelEng internal mailing list <release@mozilla.com>`__ -
`Thunderbird release drivers mailing
list <https://mail.mozilla.org/listinfo/thunderbird-drivers>`__ -
`release-automation-notifications-thunderbird mailing
list <https://mail.mozilla.org/listinfo/release-automation-notifications-thunderbird>`__
- (optional) `release-automation-notifications-dev mailing
list <https://groups.google.com/a/mozilla.com/forum/#!forum/release-automation-notifications-dev>`__

Meetings and Calendars
~~~~~~~~~~~~~~~~~~~~~~

Regular meetings are a vital part of making sure all the teams are kept
informed and consulted during the release process. To view those
meetings in your calendar you need to subscribe/be added to the
following calendars: - `Public - Release
Engineering <https://calendar.google.com/calendar/embed?src=mozilla.com_2d32343333353036312d393737%40resource.calendar.google.com>`__
(so that you attend the weekly post-mortem meeting) - `Releases
Scheduling <https://calendar.google.com/calendar/embed?src=mozilla.com_dbq84anr9i8tcnmhabatstv5co@group.calendar.google.com>`__
(so that you can attend the Tuesday/Thursday channel meetings. You can
add it following RelMan's
`docs <https://wiki.mozilla.org/Release_Management#Calendar_Updating>`__)
– If their instructions don't work, try to the “Add to Google Calendar”
button at the `web version of the
calendar <https://calendar.google.com/calendar/embed?src=mozilla.com_dbq84anr9i8tcnmhabatstv5co@group.calendar.google.com>`__.

**If you join a calendar and it's blank, you may need to delete it and
get a calendar invitation from an existing subscriber**

Documents
~~~~~~~~~

There's a simplified documentation for mid-betas and release checklists
to ease the steps needed to happen. If not already, duplicate an
existing sheet in this `google docs
checklist <https://docs.google.com/spreadsheets/d/1hhYtmyLc0GEk_NaK45KjRvhyppw7s7YSpC9xudaQZgo/edit#gid=1158959417>`__
and clear out the status that was carried over from the previous
release.

Repository and Tool Access
--------------------------

Several tools for managing releases are protected or private. In order
to do your job, you need to be granted access to a bare minimum:

-  Access to the `VPN <https://mana.mozilla.org/wiki/display/SD/VPN>`__
-  A `Bugzilla <https://bugzilla.mozilla.org/>`__ account
-  Write access to
   `releasewarrior-2.0 <https://github.com/mozilla-releng/releasewarrior-2.0/>`__
   and
   `releasewarrior-data <https://github.com/mozilla-releng/releasewarrior-data/>`__
   repo
-  Read/write access to `Balrog <https://aus4-admin.mozilla.org/>`__
-  Read access to `Ship-it v2 <https://shipit.mozilla-releng.net/>`__
-  SSH access to ``buildbot-master01.bb.releng.use1.mozilla.com``.

There are a few more other places where access is needed (such as
`bouncer <https://bounceradmin.mozilla.com/admin/>`__, etc) but we're
trying to keep those access-list short so adding can be done in time
depending on necessities.

Installing Tools
----------------

ReleaseWarrior
~~~~~~~~~~~~~~

This is the wiki for ReleaseWarrior! It helps us keep track of the
releases in flight and generating the post-mortem.

See `the releasewarrior
repo <https://github.com/mozilla-releng/releasewarrior-2.0/#installing>`__
for instructions on installation and configuration

The ``release`` command should now be available inside your virtual
environment. Other wiki pages will explain how to use it.

taskcluster
~~~~~~~~~~~

Release tasks are usually run through
`Taskcluster <https://docs.taskcluster.net/>`__, which has a useful
`Command-line
interface <https://github.com/taskcluster/taskcluster-cli>`__

-  Download an appropriate binary from
   https://github.com/taskcluster/taskcluster-cli#installation
-  Copy the binary somewhere useful, such as somewhere in your
   ```$PATH`` <http://www.linfo.org/path_env_var.html>`__
-  Make it executable, if using Mac or Linux:
   ``chmod a+x /path/to/taskcluster``
-  ``taskcluster signin`` - this will open a browser window and allow
   you to get temporary client credentials. By default this is valid for
   24 hours. **The command will display two ``export`` commands you must
   copy/paste into your shell**
-  Familiarize yourself with the subcommands, starting with
   ``taskcluster help``

Firefox bookmarks
~~~~~~~~~~~~~~~~~

These bookmarklets should help you view tasks and taskgroups in Firefox.

-  Go to Bookmarks -> Show All Bookmarks
-  Gear symbol -> New Bookmark
-  Name: ``task inspector`` Location:
   `https://tools.taskcluster.net/tasks/%s <https://tools.taskcluster.net/tasks/%s>`__
   ; Keyword: ``task``
-  Name: ``taskgroup inspector`` Location:
   `https://tools.taskcluster.net/groups/%s <https://tools.taskcluster.net/groups/%s>`__
   ; Keyword: ``taskgroup``
-  Name: ``stop`` Location: ``javascript:stop();``

   -  This can be used to stop further loading in the Task Group
      Inspector. It shouldn't be used when actively monitoring (i.e.:
      watching for failures), but it can greatly speed things up if
      you're using it for other reasons. Be sure to wait for the initial
      tasks to load before you use it.

Now if you go to your URL bar, you can type ``task TASKID`` or
``taskgroup TASKGROUPID`` and you'll go to that task or taskgroup in the
inspector.

After ReleaseDuty
-----------------

After your tour of releaseduty, it's customary to spend 1-2 weeks fixing
release automation issues. Check the `Release Automation Improvements
trello
board <https://trello.com/b/BqnBcfXX/release-automation-improvements>`__
trello board for ideas of what to work on and to add new items as you
discover them.

Ensure the next duty cycle have signed up to any phabricator reviews,
such as the periodic file updates reviews.

Miscellaneous
-------------

-  Bugzilla issues regarding specific releases/WNP are filed under
   `Release
   Engineering:Releases <https://bugzilla.mozilla.org/enter_bug.cgi?product=Release%20Engineering&component=Releases>`__
-  Issues regarding automation are filed under `Release
   Engineering:Release
   Automation <https://bugzilla.mozilla.org/enter_bug.cgi?product=Release%20Engineering&component=Release%20Automation>`__
-  The CHANGELOG in the releasewarrior-data repository contains a
   summary of larger changes made during the duty cycle.

Teams
-----

-  `Release Engineering <https://wiki.mozilla.org/ReleaseEngineering>`__
   (Releng)
-  `Release Management <https://wiki.mozilla.org/Release_Management>`__
   (Relman)
-  `Quality Assurance <https://wiki.mozilla.org/QA>`__ (QA / QE) and
   their `testing notes <https://quality.mozilla.org/>`__

Other useful resources
----------------------

-  More on `Release
   Management <https://wiki.mozilla.org/Release_Management>`__

Glossary
--------

-  WNP - The “What's New Page” can be set to appear after an upgrade, to
   tell end-users of any changes in the browser they should be aware of.
-  FF - Firefox
-  TB - Thunderbird
-  b1, b2, etc - beta release 1, beta release 2, etc

FAQ
---

1. *How does the Ship-it workflow function in terms of shipping a new
   release?*

RelMan submits a new release from
`here <https://shipit.mozilla-releng.net/>`__, another RelMan reviews
that and once it hits 'Ready' + 'Do eeaat' the release enters the
'Reviewed' section and waits to be run. Since there's a
``release-runner.sh`` script running in a loop on
`bm81 <https://hg.mozilla.org/build/puppet/file/default/manifests/moco-nodes.pp#l598>`__,
there's a max window of 60 seconds till the job gets its share,
following which it enters the 'Running/Complete' table where we can
observe its state. The “Reviewed” tab goes to “No pending release” yet
again.

2. *What does release-promotion refer to?*

'Release promotion' is simply the idea that we take an already existing
CI build from (e.g. beta) and promote that to being the build we
release/ship to users. Prior to this approach, we had always rebuilt
Firefox at the start of each new release. Long story short, release
promotion entails taking an existing set of builds that have already
been triggered and passed QA and “promoting” them to be used as a
release candidate. More on promotion can be found on our wiki
`here <https://wiki.mozilla.org/ReleaseEngineering/Release_build_promotion>`__

3. *What is the train model?*

Since 2012 Mozilla moved to a fixed-schedule release model, otherwise
known as the Train Model, in which we released Firefox every six weeks
to get features and updates to users faster and move at the speed of the
Web. Hence, every six weeks the following merges take place:
`mozilla-beta <http://hg.mozilla.org/releases/mozilla-beta/>`__ =>
`mozilla-release <http://hg.mozilla.org/releases/mozilla-release/>`__
`mozilla-central <http://hg.mozilla.org/mozilla-central/>`__ =>
`mozilla-beta <http://hg.mozilla.org/releases/mozilla-beta/>`__

We used to have an intermediate branch named 'aurora' in between central
and beta but that was brought to end-of-life during April-May 2017.
Instead, early beta releases are branded as 'DevEdition'.

4. *What is a partner repack change for FF?*

Partner repacks refer to 3rd party customized branded versions of
Firefox that Mozilla is taking care of for some of its clients. With
some exceptions, most of the partner reconfigs lie under private
repositories. Mostly, the partner repacks don't need too much of RelEng
interference as all bits are held under private git repos and are
directly handled by the partnering companies

5. *Is there calendar-based release scheduled for Thunderbird as for
   Firefox?*

No. It's irregular. Conversations happen on #tbdrivers and TB mailing
list and they trigger their release in Ship-it.

6. *Why don't I see update_verify_beta for dot releases?*

From time to time, a handful of issues precipitate a dot release. When
that happens, its behavior slightly varies from a normal release. A
normal release (e.g. 43.0, 44.0, etc) has its RC shipped to beta channel
first before making it to the release channel - for testing purposes,
update verify steps are taking place both ways, hence
update_verify_release and update_verify_beta steps. Upon a successful
testing phase we ship the RC on the beta channel and then on the release
channel, following which we merge the code for the next release cycle so
that the beta release bumps its version. In the lights of this logic, a
dot release (e.g. 43.0.1 or 44.0.1) happens a certain amount of time
after the official release. For that reason, a dot release can't be
tested in beta channel as the at-that-moment beta version is greater
than the dot release version, hence the updater would refuse to
downgrade. Therefore, there is only one cycle of update_verify for dot
releases (update_verify_release == update_verify in this case).

7. *Is there explicit signoff from RelMan for DevEdition builds?*

No, after b1, there isn't signoff from RelMan on DevEdition builds. QA
only verifies the DevEdition builds every two weeks. With the exception
of b1, and assuming all the tasks complete as expected, the DevEdition
builds should be shipped at the same time as we receive signoff for the
corresponding desktop builds.

8. *How should I inform the ReleaseDuty team of recent changes in
   automation that may impact an upcoming release?*

You can mention it to the current ReleaseDuty folks in the #releaseduty
channel. Please also add it to the upcoming release in the
../releases/FUTURE/ dir. See `future release
support <../releases/FUTURE/README.md>`__ for more details.

9. *How do I coordinate with marketing on release day?*

Join the #release-coordination channel on Mozilla Slack
