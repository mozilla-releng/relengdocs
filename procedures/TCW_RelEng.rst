.. _TCW_RelEng:
.. index:: 
    single: Tree Closing Window
    pair: Tree Closing Window; checklist
    seealso: TCW; Tree Closing Window

=============================
Tree Closing Window Execution
=============================

.. toctree::

The checklist below is for before, during, and after a Tree Closing
Window (TCW). These are the actions for almost any TCW. Most will
benefit from specific additions.

Wednesday Before
================

|_| Review any notes_ or bugs_ from prior TCWs that may be relevant.

|_| Ensure the decision on "hard close" vs. "soft close" has been made.

|_| Make sure all communications have gone out from the
:ref:`planning procedure`.

|_| Double check all bugs to be included, make sure you know how to
recover from potential issues. The CAB list is the "source of truth".


Day of TCW
==========

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
===================================

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
=================

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
