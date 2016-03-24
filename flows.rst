Flows
=====

.. _from-checkin-to-treeherder:

Firefox builds: from checkin to Treeherder
------------------------------------------

A developer checks in code to :ref:`hg.mozilla.org` using mercurial_.

:ref:`buildbot` is polling the :ref:`hg pushlog` for each of the code repositories we
do builds for using an :ref:`HgPoller`.

When the poller detects the new push, the information about the change is
written into the :ref:`scheduler database` for later processing by the
:ref:`buildbot schedulers`.

Once the schedulers have detected a new change and created new
:ref:`build requests`, the jobs are now pending_ on :ref:`Treeherder`. At this point we may `start
or create new VMs` in the cloud to service this pending work.

Once the job starts, it is now considered a running_ job on :ref:`Treeherder`.

When the job finishes, the log of all its output is collected by
:ref:`postrun.py`, and uploaded to FTP. The :ref:`status database` is then updated
with the job's final status. It is now considered :ref:`finished` on :ref:`Treeherder`.

Note that because there are several asynchronous processes at play here, a
job can disappear from the running list before it appears in the finished
list.

.. _pending: :ref:`pending jobs`
.. _running: :ref:`running jobs`
.. _finished: :ref:`finished jobs`
.. _start or create new VMs: :ref:aws_watch_pending

.. _mercurial: https://wiki.mozilla.org/Mercurial


