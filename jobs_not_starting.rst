Debugging "jobs aren't starting"
================================

One of the more common types of problems we encounter is when jobs aren't
starting properly. This document is an attempt to guide debugging efforts.

"jobs not starting" can mean a few things.

1. jobs are pending_, but not running. In this case the jobs are visible as
   pending on Treeherder_  or elsewhere.

2. jobs aren't being scheduled properly. In this case, the jobs aren't
   visible as pending anywhere. Their triggers appear to be working, but
   the jobs themselves aren't being created.

----------------------------
pending jobs aren't starting
----------------------------
In the first case, the jobs are being created in the database properly, but
aren't being started.

This could be due to invalid buildbot configuration or reconfig.

Some possible issues:

- Were the scheduler masters reconfigured but not the build/test masters?
  Perhaps the reconfig of the build/test masters failed?

- Does any master actually run those builders? Check allthethings.json_.
  Maybe production-masters.json_ wasn't updated with the appropriate
  platforms or branches?

If buildbot has the builder enabled, but jobs aren't starting, next check
twistd.log on the master. Some things to look for:

- "prioritizeBuilders: ... removed builder XXX with no allocated slaves
  available". This means there were pending jobs for XXX, but no slaves
  attached to the master that could do it.

- "<Builder ''XXX'' at YYYYYY>: want to start build, but we don't have a
  remote". Similar to above. No slaves were found to do the job.

These messages can mean that there are no slaves attached and idle to do
the job, but it can also mean that the slave selection function (aka
"nextSlave") isn't selecting one of the connected slaves for some reason.
Other things to watch out for:

- Is the builder in a jacuzzi or not? Check the list of `jacuzzi'ed
  builders`_. See also https://wiki.mozilla.org/ReleaseEngineering:Jacuzzis
  for debugging jacuzzis. Perhaps the allocation is too small, in which
  case all the specified slaves would be online and busy. To address this,
  increase the allocation for this builder.

  Perhaps the allocated slaves aren't functional for some reason. Check
  that they're being started correctly in aws_watch_pending.log_ and the
  AWS console.

- "nextAWSSlave Waiting for inhouse slaves to show up". There's a short
  (60s) timeout where we'll try and wait for any in-house slaves to take
  the job before giving it to an AWS slaves.

Jobs not starting can also be a symptom of general capacity issues.

First thing to do is identify what kinds of machines aren't starting, and
if they have anything in common. For example, is the problem specific to
AWS machines? AWS machines of a particular type? Test slaves? Tegras? Be on
the lookout for exceptions to your hypothesis, as the exceptions often
indicate where the root of the problem is.

AWS slaves not starting? Try checking:

- aws_watch_pending.log_. Any unhandled errors? We could be at our capacity
  limits. Perhaps spot prices have risen everywhere and we aren't able to
  get enough instances. We have self-imposed limits in watch_pending.cfg_.
  In addition, each AWS slave needs a buildbot name assigned to it, so the
  list of machines in slavealloc_ and buildbot-configs_ needs to be large
  enough.

- AWS console. Particularly check the `spot instances section`_. Errors
  creating spot instances aren't immediately apparent in
  aws_watch_pending.log

.. _aws_watch_pending.log:

`aws_watch_pending.log` is available on aws-manager1.srv.releng.scl3.mozilla.com:/builds/aws_manager/aws_watch_pending.log


---------------------------
jobs aren't being scheduled
---------------------------
The most likely thing here is a scheduling issue. Perhaps the jobs were
inadvertently removed by a recent patch. In this case one particular type
of job will be missing, but other types will be fine.

The other likely culprit is the scheduler masters are hung or really busy.
In this case, new jobs will be very slow to be scheduled. Possible causes
for this include:

- Network between scheduler masters and DB is bad

- DB is slow, or blocked by some long running queries

- Scheduler masters are stuck processing lots of old changes. This can
  happen if we re-enable a scheduler that has been disabled for a while.
  Normally these should be cleaned up, but it's possible the cleanup
  process missed it, or it wasn't old enough to be deleted, but was old
  enough to cause problems.


.. _pending: :ref:`pending jobs`
.. _Treeherder: :ref:`Treeherder`
.. _allthethings.json: http://builddata.pub.build.mozilla.org/reports/allthethings.json
.. _production-masters.json: http://hg.mozilla.org/build/tools/raw-file/default/buildfarm/maintenance/production-masters.json
.. _jacuzzi'ed builders: http://jacuzzi-allocator.pub.build.mozilla.org/v1/builders/
.. _spot instances section: https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#SpotInstances:
.. _watch_pending.cfg: http://hg.mozilla.org/build/cloud-tools/file/5ae7cdc4796e/configs/watch_pending.cfg
.. _slavealloc: :ref:`slavealloc`
.. _buildbot-configs: http://hg.mozilla.org/build/buildbot-configs
