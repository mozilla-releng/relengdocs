.. _software:

Software
========

.. _buildbot:

Buildbot
--------

Buildbot Overview
~~~~~~~~~~~~~~~~~

If you are new to Buildbot, please follow this excellent tutorial:  `Buildbot in 5 min`_. If you end
up lost or want more information on Buildbot itself, check out the full `Buildbot Docs`_.

Buildbot automates the following repetitive process:

1. recognizing when changes land in your application's source code
2. building/installing your software against changed source code across all supported platforms
3. running tests on the newly build software
4. storing the output and results (status) of how everything went.

By no means is it restricted to this but that's a general use case of Buildbot.

Now let's take a practical example in Mozilla where this would apply:

1. A developer pushes a commit to the mozilla-central repo.
2. Firefox is then installed on all our supported versions of Windows, Mac os x, Linux, and Android.
3. All tests and profiling suites (mochitests, reftests, talos, etc) are then ran against each newly build Firefox.
4. Logs are uploaded to :ref:`TBPL`, with status of how everything went.

Buildbot has a concept of masters and slaves. As the names imply, the masters are the brains, and the slaves are the headless chickens who are told what to do.

Let’s take a simple scenario. You have a few machines with Buildbot installed and you construct them as “Buildbot Slaves”. Then, on another machine, you
construct a "Buildbot Master". The master and slaves connect and the master will eventually do things like ‘hey slave, install Firefox against this revision of
source’. Slaves don’t know how to do this and it will be up to the master to communicate how that’s done with specific commands(steps). Generally, Buildbot
Masters are configured so that they know how to do everything: what repos to watch, how to prioritize and schedule builds, what slaves it has in its control and
what builds they are capable of building.

Mozilla Releng and Buildbot
~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
:ref:`build requests`. Some usual examples of this are creating the
requests to do builds in response to a developer push, or doing nightly
builds on a timer.

Schedulers themselves are run sequentially in a loop on the `buildbot
master`. They are generally run on a timer, or if a new buildbot change is
added to the master.

Schedulers that use push information generally look in the
:ref:`scheduler database` for new changes since last time the scheduler
ran. If there are any new changes that are applicable, the scheduler
then creates new rows in the buildrequests table of the :ref:`scheduler
database`.

In addition to the `built-in schedulers`_, RelEng maintains many custom
buildbot schedulers.

aggregating scheduler

pgo scheduler

per-product scheduling

coalescing

Commonly Used Built-In Schedulers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Periodic`_:
    Runs a build at a certain interval, starting at time of builder
    creation (scheduler startup).

`Nightly`_:
    Runs a build at a specific time.

.. _built-in schedulers:
   http://hg.mozilla.org/build/buildbot/file/production-0.8/master/buildbot/schedulers
.. _`Periodic`:
    http://hg.mozilla.org/build/buildbot/file/production-0.8/master/buildbot/schedulers/timed.py#l66
.. _`Nightly`:
    http://hg.mozilla.org/build/buildbot/file/production-0.8/master/buildbot/schedulers/timed.py#l119

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
log for the job, uploading it to ftp, updating the :ref:`status
database` and pushing the final notification events to pulse.

http://hg.mozilla.org/build/buildbotcustom/file/default/bin/postrun.py


Mozharness
----------

Mozharness is a configuration driven script harness. It provides a set of common tools for writing scripts. These scripts know how to do some general task that is agnostic to specifics: platform or special variants. The scripts get their specific details from a corresponding config.

eg: you could a have a script that is tasked with running a Firefox test suite: a windows 7 mochitest plain1 build

Basescript: Basescript is the core of Mozharness. It defines how scripts are run. Basescript is also responsible for
self.config. self.config is the config dict that represents a given script run. The logic for populating self.config happens via BaseConfig. BaseConfig will
conglomerate variables like default_config (a dict that represents some default items that all scripts will use), config files (eg: when you pass --cfg
config_file.py, we grab the dict from that file), and other command line args (eg: --branch mozilla-central, could do self.config['branch'] = 'mozilla-central')



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
http://hg.mozilla.org/build/buildapi (`buildapi docs`_)

.. _`buildapi docs`: http://moz-releng-docs.readthedocs.org/projects/moz-releng-buildapi

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
.. _Buildbot Docs: http://docs.buildbot.net
.. _Buildbot in 5 min: http://docs.buildbot.net/current/tutorial/fiveminutes.html

