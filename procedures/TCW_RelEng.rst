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


|_| Make sure all communications have gone out from the
:ref:`planning procedure`.

|_| Double check all bugs to be included, make sure you know how to
recover from potential issues. The CAB__ list is the "source of truth".

|_| make sure you are in the Owners group within
https://github.com/mozilla-b2g/gaia/settings/collaboration

__ https://docs.google.com/a/mozilla.com/spreadsheet/ccc?key=0AuW-f5fEg7u4dGN0QUE1NERiNVdjSjZoN1RxWVRrWnc#gid=4

Day of TCW
==========

|_| Check and screenshot various dashboards to see what is current "normal".

    - |_| Check `nagios service dashboard`__ 
    - |_| Screenshot `nagios tacktical dashboard`__ 
    - |_| Screenshot `slavehealth`__

__ https://nagios.mozilla.org/releng-scl3/cgi-bin/status.cgi?servicegroup=all&style=summary
__ https://nagios.mozilla.org/releng-scl3/cgi-bin/tac.cgi
__ https://secure.pub.build.mozilla.org/builddata/reports/slave_health/index.html

|_| (optional) post message in IRC channels in advance. Usually #mobile,
#b2g, #developers, #releng, and #gaia. Sample::

    REMINDER - Trees close in about 1 hour for https://bugzil.la/1087431

|_| Pull up local copies of all bugs and the etherpad, in case of
network issues (planned, or unplanned)

|_| Log in to the primary and backup IRC channels, see `IT IRC usage`__,
make sure you have latest passwords.

__ https://mana.mozilla.org/wiki/display/SYSADMIN/IRC+use+within+IT

|_| Touch base with the MOC "on duty" person about 15 minutes before
scheduled start of TCW.

|_| Close the trees with the tracker bug URL mentioned. (For "non-tree
closing" TCW, select all the open branches and add the message "TCW in
process, devs need to handle their own restarts", and "open" them saving
state.)

|_| In addition, we need to actually close Gaia. You need to be in the Owners group.
Go the Github settings page and remove the Chefs and Cooks teams from the
collaborators listing: https://github.com/mozilla-b2g/gaia/settings/collaboration
Once the TCW is completed, they can be re-added to "open" Gaia once again.

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

.. |_| raw:: html

    <input type="checkbox" />

.. |X| raw:: html

    <input type="checkbox" checked />
