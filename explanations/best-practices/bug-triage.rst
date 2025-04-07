Bug Triage
==========

This page outlines the process for triaging open RelEng bugs in `Bugzilla <https://bugzilla.mozilla.org/home>`_. The procedure ensures a well-organized bug database, where each bug is appropriately tagged and prioritized, making full use of Mozilla's `Bugdash <https://bugdash.moz.tools/?team=RelEng>`_ triage tool.

Goals of Bug Triage
-------------------

1. Close irrelevant bugs.
2. Maintain the status of active bugs, ensuring they are correctly labeled and marked as triaged.
3. Identify suitable candidates for 'good-first-bugs'.
4. Identify 'low-hanging-fruits' with quick resolutions.
5. Ensure bugs are considered triaged according to the Firefox triage process.

This process is influenced by the :external:doc:`Firefox triage process <bug-mgmt/policies/triage-bugzilla>`. However, we've adapted the definitions of bug severity to suit our needs.

Bug Fields
----------

Severity
^^^^^^^^

This field describes the impact of a bug and is utilized to determine the scope of a bug’s effect on the Firefox release pipeline. Severity is used as input for setting the priority of a bug.

==========  =======================================================================
Value       Description
==========  =======================================================================
--          This is the default value for new bugs. Bug triagers for components
            (i.e., engineers and other core project folks) are expected to update
            the bug's severity from this value. To avoid missing new bugs for
            triage, this default should not be altered when filing bugs.
S1          (Catastrophic) Halts releases from being shipped. This is the highest
            priority for releaseduty.
S2          (Serious) Hinders specific steps in the release pipeline but does not
            prevent a release from being shipped.
S3          (Normal) Issues that are intermittent or can be manually worked
            around without much hassle.
S4          (Small/Trivial) Minor significance, cosmetic issues, low or no impact
            on users.
N/A         (Not Applicable) The above definitions do not apply to this bug; this
            value is reserved for bugs of type 'Task' or 'Enhancement'.
==========  =======================================================================

Priority
^^^^^^^^

This field describes the importance and order in which a bug should be fixed compared to other bugs.

==========  =======================================================================
Value       Description
==========  =======================================================================
--          No decision
P1          Fix in the current release cycle
P2          Fix in the next release cycle or the following (nightly + 1 or nightly + 2)
P3          Backlog
P4          Do not use. This priority is for the Web Platform Test bot.
P5          Will not fix, but will accept a patch
==========  =======================================================================
