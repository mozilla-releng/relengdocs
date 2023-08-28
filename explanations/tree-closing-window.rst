Tree Closing Window
===================

The purpose of the Planning Procedure below is to state 
the de facto agreement on the process for Tree Closing
Windows (TCW). A few enhancements will be proposed along the way *in
italics*.

.. _planning procedure:

Planning Procedure
------------------

The goal is to have all the workload, durations, and personnel
assignments done at least one week in advance of the TCW.

* All requests for work during a TCW must be submitted to CAB_ no later
  than 2 meetings prior to the TCW. (This is typically 10 days.)

    - Late requests that extend the TCW will be denied unless they are
      emergency.

    - Late requests that fit within the planned window will be denied
      unless there is good reason for the lateness. Even so, they may be
      denied if personnel changes would be needed.

    - Late requests that do not require a tree closure are up to IT to
      decide.

* All requests must include (handled as part of the CAB_ Change Request
  process):

    - Steps and duration for "all goes well".
    - Steps and duration for rollback.
    - Assistance needed (specifically). E.g. "zeus expert" or "buildapi
      expert"

* There is no official calendar of potential TCW dates (in part because
  there is no official calendar of release dates). A TCW date is
  calculated as follows:

    - The master schedule is driven off the `official release`_
      schedule. Usually, TCW is the 3rd Saturday after Firefox release,
      but may be the 4th with pre-arrangement with Release Management.

* No later than 2 Fridays preceding the TCW (8 days), the composite
  time line will be established and documented in a spreadsheet.

    .. note:: Tracking Bug

        The tracking bug summary should be updated with the planned
        start and completion times of the TCW.

    .. note:: Early Viewing

        An early view of what has been requested for the next TCW can be
        seen via the `TCW Requests`_ link into Service Now.

* As soon as the list of activities is determined, RelEng can make a
  determination whether the TCW can use a "soft close" or a "hard
  close".

* No later than end-of-day Wednesday preceding the downtime, RelEng
  constructs an email
  announcement, based on the text posted on `internal status`_ by MOC.
  That email is cross posted to the appropriate engineering lists.
  (Currently, that is dev-planning, dev-tree-management,
  dev-platform.)

  .. note:: RelEng Contact Posts to Newsgroups

      The MOC will publish a note on the internal status page describing
      the changes. However, they do
      not have posting privileges to the newsgroups. Therefore the RelEng
      contact person posts (forwards) on the MOC's behalf, adding any
      addition information (such as "soft close" status). Even if the
      MOC email is sent to everyone, we still post to newsgroups to
      reach community members of the development community.

.. _CAB: https://mana.mozilla.org/wiki/display/MOC/Change+Advisory+Board
.. _official release: https://wiki.mozilla.org/RapidRelease/Calendar
.. _TCW Requests: https://mozilla.service-now.com/nav_to.do?uri=%2Fsys_report_template.do%3Fjvar_report_id%3D012b81bbdb0e26006c3fb1c0ef9619e1%26jvar_selected_tab%3DmyReports%26jvar_list_order_by%3D%26jvar_list_sort_direction%3D%26sysparm_reportquery%3D%26jvar_search_created_by%3D%26jvar_search_table%3D%26jvar_search_report_sys_id%3D%26jvar_report_home_query%3D
.. _Internal Status: https://mozilla2.statuspage.io/

Tree Closing Window Execution
=============================

The MOC administers the TCW. In general, the following generally occur:

* Spreadsheet with name of person on the hook for each bug and support
  group created. Links and any special contact info should be in the
  pad.

* Planned timeline in the spreadsheet.

* Communication channels defined. Usually irc (#moc),
  backup irc (freenode #mozilla-it), Vidyo (MOC) if needed.

* Designated person to run the TCW. Usually the on-call MOC staffer.

* Spreadsheet is kept current with status, including times.

* All people involved with a tree closing part of the window remain
  on call until the trees are reopened.

The checklist below is for before, during, and after a Tree Closing
Window (TCW). These are the actions for almost any TCW. Most will
benefit from specific additions.

Wednesday Before
----------------

|_| Review any notes_ or bugs_ from prior TCWs that may be relevant.

|_| Ensure the decision on "hard close" vs. "soft close" has been made.

|_| Make sure all communications have gone out from the
:ref:`planning procedure`.

|_| Double check all bugs to be included, make sure you know how to
recover from potential issues. The CAB list is the "source of truth".


Day of TCW
----------

|_| Check and screenshot various dashboards to see what is current "normal".

    - |_| Check `nagios service dashboard`__
    - |_| Screenshot `nagios tactical dashboard`__
    - |_| Screenshot `slavehealth`__

__ https://nagios.mozilla.org/releng-scl3/cgi-bin/status.cgi?servicegroup=all&style=summary
__ https://nagios.mozilla.org/releng-scl3/cgi-bin/tac.cgi
__ https://secure.pub.build.mozilla.org/builddata/reports/slave_health/index.html

|_| (optional) post message in IRC channels in advance. Usually #mobile,
#developers, and #releng. Sample::

    REMINDER - Trees close in about 1 hour for https://bugzil.la/1087431

|_| Pull up local copies of all bugs and the spreadsheet, in case of
network issues (planned, or unplanned)

|_| Log in to the primary and backup IRC channels, see `IT IRC usage`__,
make sure you have latest passwords.

__ https://mana.mozilla.org/wiki/display/SYSADMIN/IRC+use+within+IT

|_| Touch base with the MOC "on duty" person about 15 minutes before
scheduled start of TCW.

|_| Close the trees with the tracker bug URL mentioned. (For "soft tree
closing" TCW:

    - |_| Hard close autoland first.

    - |_| Select all the open branches and add the message "TCW in
      process, devs need to handle their own restarts", and "open" them
      saving state.

When TCW Done, Before Opening Trees
-----------------------------------

|_| Check `nagios dashboard`__ that all is as expected.

__ https://nagios.mozilla.org/releng-scl3/

|_| Check build API for `pending`__, `running`__, and `recent`__ to
ensure those system are up.

__ https://secure.pub.build.mozilla.org/buildapi/pending
__ https://secure.pub.build.mozilla.org/buildapi/running
__ https://secure.pub.build.mozilla.org/buildapi/recent

|_| Check `Treeherder`__ to ensure it is up.

__ https://treeherder.mozilla.org/

|_| Reopen regular trees.

|_| Reopen autoland (if closed for this TCW).

|_| Update notes_ and file bugs_ as appropriate to capture any issues.
Invite all TCW participants to do the same.

Next Business Day
-----------------

|_| Review any notes_ or bugs_, and ensure they have enough context.

|_| File Bugzilla tickets for any work that must be done. Put a link to
the Bugzilla ticket in the GitHub issue, but do not close the issue
until the bug is fixed.

.. _notes: https://github.com/mozilla-releng/TCW-history/wiki
.. _bugs: https://github.com/mozilla-releng/TCW-history/issues

.. |_| raw:: html

    <input type="checkbox" />

.. |X| raw:: html

    <input type="checkbox" checked />
