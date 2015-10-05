.. _TCW:
.. index:: 
    single: Tree Closing Window
    seealso: TCW; Tree Closing Window

============================
Tree Closing Window Planning
============================

The purpose of the Planning Procedure below is to state what I believe
to already be the de facto agreement on the process for Tree Closing
Windows (TCW). A few enhancements will be proposed along the way *in
italics*.

Once we're in agreement, we can make it more public, to avoid surprises
all around.

.. _planning procedure:

Planning Procedure
==================

The goal is to have all the workload, durations, and personnel
assignments done at least one week in advance of the TCW.

* All requests for work during a TCW must be submitted to CAB no later
  than 2 meetings prior to the TCW. (This is typically 10 days.)

    - Late requests that extend the TCW will be denied unless they are
      emergency.

    - Late requests that fit within the planned window will be denied
      unless there is good reason for the lateness. Even so, they may be
      denied if personnel changes would be needed.

    - Late requests that do not require a tree closure are up to IT to
      decide.

* All requests must include:

    - Steps and duration for "all goes well".
    - Steps and duration for rollback.
    - Assistance needed (specifically). E.g. "zeus expert" or "buildapi
      expert"

* IT will keep the Engineering informed of TCW status via the
  Engineering meeting run by Lawrence Mandel. (`Typical Agenda`__)

__ https://wiki.mozilla.org/Platform/2013-10-15

* *Announcements of TCW times will occur in EngOps meeting.*

* *A calendar of next two TCWs will be maintained, including tracker
  bugs.*

* *No later than 2 Fridays preceding the TCW (8 days), the composite
  time line will be established and documented in an ether pad.* This
  ensures accurate information can be provided at various engineering
  meetings the week prior to the TCW.

    .. note:: Tracking Bug

        The tracking bug summary should be updated with the planned
        start and completion times of the TCW.

    .. note:: Releng Access

        Not all RelEng folks are able to access the infra etherpads. The
        etherpad should be password protected, and internet viewable,
        prior to the TCW.

    .. note:: Etherpad Access

        If there is a chance that Etherpad will be affected by the TCW,
        a Google Doc should be set up instead.

* *No later than end-of-day Wednesday preceding the downtime, email
  announcement, cross posted to the appropriate engineering lists, will
  be sent out.* (Typically, that is dev-planning, dev-tree-management,
  dev-platform, dev-fxos.)

Execution of TCW
================

We've had the most consistent success when the following practices were
followed:

* Ether pad with name of person on the hook for each bug and support
  group created. Links and any special contact info should be in the
  pad.

* Planned timeline in the ether pad.

* Communication channels defined. Usually Vidyo (NOC), irc (#it,
  #infra), backup irc (freenode #mozilla-it).

* Designated person to run the TCW. Usually the oncall SE *(if they
  don't have too much work to do during TCW)*.

* Etherpad kept current with status, including times.

* All people involved with a tree closing part of the window remain
  on call until the trees are reopened.
