.. _TCW:
.. index:: 
    single: Tree Closing Window
    seealso: TCW; Tree Closing Window

============================
Tree Closing Window Planning
============================

The purpose of the Planning Procedure below is to state 
the de facto agreement on the process for Tree Closing
Windows (TCW). A few enhancements will be proposed along the way *in
italics*.

.. _planning procedure:

Planning Procedure
==================

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

Execution of TCW
================

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

See :ref:`detailed checklist<TCW_Releng>` for actions to be taken.

.. _CAB: https://mana.mozilla.org/wiki/display/MOC/Change+Advisory+Board
.. _approved changes: https://mozilla.service-now.com/sys_report_template.do?jvar_report_id=dee1b20913c5aa00472ed2f18144b068&jvar_selected_tab=myReports&jvar_report_home_query=
.. _official release: https://wiki.mozilla.org/RapidRelease/Calendar
.. _TCW Requests: https://mozilla.service-now.com/nav_to.do?uri=%2Fsys_report_template.do%3Fjvar_report_id%3D012b81bbdb0e26006c3fb1c0ef9619e1%26jvar_selected_tab%3DmyReports%26jvar_list_order_by%3D%26jvar_list_sort_direction%3D%26sysparm_reportquery%3D%26jvar_search_created_by%3D%26jvar_search_table%3D%26jvar_search_report_sys_id%3D%26jvar_report_home_query%3D
.. _Internal Status: https://mozilla2.statuspage.io/
