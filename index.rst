.. title:: RelEng: The Docs

=================
Table of Contents
=================
.. contents::

=====
Flows
=====

------------------------------------
Firefox builds: from checkin to TBPL
------------------------------------

A developer checks in code to `hg.mozilla.org`_ using mercurial_.

buildbot_ is polling the `hg pushlog`_ for each of the code repositories we
do builds for using an HgPoller_.

When the poller detects the new push, the information about the change is
written into the `scheduler database`_ for later processing by the `buildbot
schedulers`_.

Once the schedulers have detected a new change and created new `build
requests`_, the jobs are now pending_ on TBPL_. At this point we may `start
or create new VMs`_ in the cloud to service this pending work.

Once the job starts, it is now considered a running_ job on TBPL_.

When the job finishes, the log of all its output is collected by
postrun.py_, and uploaded to FTP. The `status database`_ is then updated
with the job's final status. It is now considered finished_ on TBPL_.

Note that because there are several asynchronous processes at play here, a
job can disappear from the running list before it appears in the finished
list.

.. _pending: `pending jobs`_
.. _running: `running jobs`_
.. _finished: `finished jobs`_
.. _start or create new VMs: aws_watch_pending_

.. _mercurial: https://wiki.mozilla.org/Mercurial

.. include:: hosts.rst

.. include:: software.rst
