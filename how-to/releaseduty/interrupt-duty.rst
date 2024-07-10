Interrupt Duty
==============

An important element of ReleaseDuty is shielding the rest of the team from
interrupts as best as possible. The idea is that no single person should be
overwhelmed by interrupts, and by taking turns being held responsible for them
(via ReleaseDuty), we can minimize the risk of burn out.

Interrupts could be anything from a simple ~5 min fxci-config request, to
larger requests that need to be triaged, to full scale emergencies.

Run Book
--------

This run book can help everyone figure out how to field requests and when to
escalate.

For InterruptDuty
~~~~~~~~~~~~~~~~~

1. Upon receiving an interrupt (either request or emergency), create a JIRA
   ticket to track it.

    a. If it fits nicely in one of our epics, add the appropriate epic link
       (otherwise assign it to `Issues Without Epics`).
    b. Ensure ticket has the ``interruptduty`` label attached.
    c. Ensure ticket has a priority.
        i. If request is urgent, assign priority `Highest`.
        ii. If unsure, work with other stakeholders on the team to determine it.

    d. Determine if interrupt has a deadline and set `Due Date` field accordingly.
    e. Ensure additional context (bugs, issues, etc) are linked from the description.
        i. If no bug or issue exist and discussion with external stakeholders
           may be required, consider filing a bug / issue (or ask requester to do
           so).

2. If interrupt is low / medium priority, no further action is required.

    a. If useful, raise the interrupt at appropriate meeting(s) or directly
       with stakeholders on the team.

3. If interrupt is high priority (but not highest) or has a hard deadline
   within 3 months:

    a. Move the ticket to the ``Next`` column.
    b. Work to find an owner for it.
    c. These interrupts should be in the ``Next`` column and should be on someone’s
       radar to tackle soon.
    d. These are not necessarily the responsibility of InterruptDuty to fix.

4. If interrupt is highest priority:

    a. These interrupts are in the Expedite swim lane and should have an
       assignee responsible for working on it ASAP.
    b. If person on InterruptDuty is capable of handling request, they should be assignee.
    c. Otherwise, they should work closely with assignee to provide support /
       cross-train to better handle request in the future

For everyone else
~~~~~~~~~~~~~~~~~

1. If you notice a general request in a channel, CC InterruptDuty by mentioning
   the ``relduty`` keyword.
2. If you are pinged directly (whether in channel, DM, e-mail, bug, etc):

  a. If it is small (less than 2 hours) and you have the time, knowledge and
     desire to handle it, feel free to just handle it.
  b. Otherwise, redirect request to InterruptDuty.
