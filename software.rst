Software
========

.. _buildbot:

buildbot
--------

RelEng is currently using a patched version of buildbot 0.8.2. Our
repository is located at http://hg.mozilla.org/build/buildbot.

Upstream buildbot is currently located at
https://github.com/buildbot/buildbot/.

universal master; scheduler master; build/test master

slave deployment

https://wiki.mozilla.org/ReleaseEngineering/Landing_Buildbot_Master_Changes

.. _pushlog:
.. _`hg pushlog`:

hg pushlog
----------
Mozilla maintains a record of when changes are pushed into various
repositories on `hg.mozilla.org`_. This is currently implemented in the
`pushlog.py hook`_ 

The pushlog has several interfaces of interest, the html view which is
useful to developers, and the json format which is more useful for
automated systems.


.. _pushlog.py hook: http://hg.mozilla.org/hgcustom/hghooks/file/15e5831ab26b/mozhghooks/pushlog.py
.. _`buildbot schedulers`:

buildbot schedulers
-------------------
Buildbot schedulers are objects that are responsible for creating new
`build requests`_. Some usual examples of this are creating the requests to
do builds in response to a developer push, or doing nightly builds on a
timer.

Schedulers themselves are run sequentially in a loop on the `buildbot
master`. They are generally run on a timer, or if a new buildbot change is
added to the master.

Schedulers that use push information generally look in the `scheduler
database`_ for new changes since last time the scheduler ran. If there are
any new changes that are applicable, the scheduler then creates new rows in
the buildrequests table of the `scheduler database`_.

In addition to the `built-in schedulers`_, RelEng maintains many custom
buildbot schedulers.

aggregating scheduler

pgo scheduler

per-product scheduling

coalescing

.. _built-in schedulers:
   http://hg.mozilla.org/build/buildbot/file/d1b15ab18f40/master/buildbot/schedulers

.. _HgPoller:

HgPoller
--------
http://hg.mozilla.org/build/buildbotcustom/file/a9f6adc7dcbb/changes/hgpoller.py

l10n

tipsonly

mergepushchanges

maxchanges

.. _`postrun.py`:

postrun.py
----------

postrun.py is run after most jobs. It is reponsible for creating the text
log for the job, uploading it to ftp, updating the `status database`_ and
pushing the final notification events to pulse.

http://hg.mozilla.org/build/buildbotcustom/file/default/bin/postrun.py


.. _TBPL:

TBPL
----
https://wiki.mozilla.org/Sheriffing/TBPL

https://tbpl.mozilla.org/

https://wiki.mozilla.org/Tinderboxpushlog

https://hg.mozilla.org/webtools/tbpl/file/tip/README

https://wiki.mozilla.org/TbplWebsiteDoc

?showall=1
?jobname=foo

https://hg.mozilla.org/webtools/tbpl/

treeherder

.. _buildapi:

buildapi
--------
http://hg.mozilla.org/build/buildapi

https://wiki.mozilla.org/ReleaseEngineering/BuildAPI


Cloud tools
-----------
http://hg.mozilla.org/build/cloud-tools/

aws_watch_pending
~~~~~~~~~~~~~~~~~
http://hg.mozilla.org/build/cloud-tools/file/1e02720fa840/aws/aws_watch_pending.py

aws_stop_idle
~~~~~~~~~~~~~
http://hg.mozilla.org/build/cloud-tools/file/1e02720fa840/aws/aws_stop_idle.py

.. _hg.mozilla.org: https://hg.mozilla.org

VCS Sync tools
--------------


.. index:: single: vcs2vcs; legacy

legacy
~~~~~~

The legacy (first implementation) code is in:
    http://hg.mozilla.org/users/hwine_mozilla.com/repo-sync-tools/

The legacy configurations are in:
    http://hg.mozilla.org/users/hwine_mozilla.com/repo-sync-configs/

Documentation is in the code repository, a rendered version of the
latest is at https://people.mozilla.org/~hwine/tmp/vcs2vcs/index.html

Databases
---------

.. .. include:: schedulerdb.rst
.. .. include:: statusdb.rst

