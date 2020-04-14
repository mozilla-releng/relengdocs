Puppet pyup merges
==================

CIDuty is currently assisting with pyup updates to the puppet repo. They
regularly need help with these. This is a document to help releaseduty
help CIDuty with these merges.

It may be a good idea to read through this document before making
changes.

Get the PR into good shape
==========================

The first part is to get the PR in good shape. For these PRs especially,
the taskcluster task results are important. These tests verify that the
modules are all compatible with each other, with the caveat that the
``nodownload`` packages may be ignored.

Upstream pins that don’t match latest
-------------------------------------

For upstream pins that don’t match latest, we need to find the version
that will work. For example, the test revealed the error

::

   /build-puppet/modules/transparency_scriptworker/files/requirements.txt: taskcluster 5.0.0 has requirement taskcluster-urls<11,>=10.1.0, but you'll have taskcluster-urls 11.0.0 which is incompatible.

This is due to `this
line <https://github.com/taskcluster/taskcluster-client.py/blob/552360fbaec7b577ad5b8b26fe0d1ad130b6ef6d/setup.py#L33>`__.
To fix, we had to downgrade ``taskcluster-urls`` to ``10.1.0``.

We can either use the previous-good version, or we can `search
pypi <https://pypi.org/search/?q=taskcluster-urls>`__ for the package
and look at the `release
history <https://pypi.org/project/taskcluster-urls/#history>`__.

requirements files with stale ``ignore``\ s or pins
---------------------------------------------------

We may have pinned the upstream-of-upstream module in the puppet
requirements files themselves. For example, if ``module1==1.5.0``
requires ``module2<3.0``, we may have pinned ``module2==2.0.1`` with a
``# pyup: ignore`` or a ``# pyup: <3.0``. However, when ``module1``
bumps to a new version, that new version may require ``module2>=3.0``.
If we leave this, we may never be able to update either. If we catch
this, we can try updating both ``module`` and ``module2``.

When to land
============

Because of the nature of our puppet deployments, we may see hiccups in
services during puppet deployment. For instance, if we update the
``signing_scriptworker`` requirements, when those instances puppetize,
we may see failures in signing tasks.

We probably want to avoid landing these puppet updates during or right
before chemspills or other critical releases. Other than that, we likely
want to merge when we have time to monitor the puppet mail and help deal
with fallout.

Landing
=======

When we land, CIDuty will monitor treeherder and puppet mail. It may be
a good idea for us to keep an eye on ``#ci`` and puppet mail as well. If
we hit errors,
`papertrail <https://papertrailapp.com/groups/1141234/events?q=puppet-agent>`__
can be helpful.

Module downloads
----------------

When we land a new change to the requirements files, puppet will
download any missing modules. There is often a gap between 1) the first
machines trying to puppetize with the new requirements files, and 2) the
module being available on the puppet servers, so there is likely going
to be a wave of puppet failures immediately following a pyup merge.

We need to make sure that these clear up within a puppet pass or two, or
there may be something wrong.

Downloading the wrong wheel
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Wheels are preferable for installation, but our download script doesn’t
cover downloading all the versions of every wheel we need.

For instance, sometimes a wheel is good for any python or platform. For
example, ``urllib3-1.24-py2.py3-none-any.whl`` is good for python2 or
python3, for any platform on any architecture. If the wheel contains
compiled code, it may be more restrictive. For example,
``yarl-1.2.6-cp36-cp36m-manylinux1_x86_64.whl`` is compiled for cpython
3.6, linux, on 64bit intel type CPUs. If we’re on a different python
(3.7, 3.5), a different platform (mac), or different architecture (arm
or 32 bit), pip won’t use that wheel.

If pip is complaining about not finding a matching file, one way to
debug is

-  ssh ``releng-puppet2.srv.releng.mdc1.mozilla.com``

-  for python2, ``cd /data/python/packages``; for python3,
   ``cd /data/python/packages-3.x``

-  look for the package name that’s missing. Note that pip will treat a
   dash ``-`` the same as an underscore ``_`` in the package name, so
   ``python-jose`` is the same module as ``python_jose``, for example.
   If we’re missing, say, the mac wheel (we only have a ``manylinux1``
   wheel for that module + version), we should download it:

-  search for the module name on `pypi <https://pypi.org/>`__

-  click on the correct module,
   e.g. `yarl <https://pypi.org/project/yarl/>`__

-  if the latest version doesn’t match the version we want, find it in
   the release history, e.g. `yarl release
   history <https://pypi.org/project/yarl/#history>`__; click on the
   correct version

-  look at the download files for the wheel with the correct python
   version, platform, and arch. If there is no such wheel, go for the
   source tarball or zip.

I tend to download this into my homedir and move it into the correct
repo, e.g.

::

   pushd ~
   wget https://...
   cd /data/python/packages-3.x  # for 3.x packages; otherwise /data/python/packages
   sudo mv -n ~/FILENAME .  # sudo allows me to write in the repo dir;
                            # mv -n doesn't overwrite an existing file

Puppet will rsync this file around. Once the correct file exists on any
puppet master, pip should be able to find it.

Other download problems
~~~~~~~~~~~~~~~~~~~~~~~

There may be download problems if we point at a version or module that
doesn’t exist on pypi. The fix here probably involves creating a new PR
to point to the right module version, and merging it.

“stuck” installs
~~~~~~~~~~~~~~~~

There may be a compile problem, a configuration problem, a dependency
issue, or other.

First, is this affecting an entire class of machines, or just one
machine? This is hard to tell when dealing with singleton pools, but if
all signing scriptworkers are fine except for one, then it’s likely a
machine issue. If all signing scriptworkers are throwing an error during
puppetizing, then it’s probably a puppet issue.

Puppet’s ``pip`` logging can be a bit terse, but it shows you the
commandline used. If you log into an affected machine and try to run
that ``pip`` command manually, you may get a better sense of what’s
wrong, possibly adding the ``-v`` option to be more verbose, e.g.

::

   # You want to be su'ed as the user that owns /builds/scriptworker, probably cltbld or cltsign
   /builds/scriptworker/bin/pip -v install --no-deps --no-index  --find-links=https://releng-puppet1.srv.releng.usw2.mozilla.com/python/packages-3.x --trusted-host releng-puppet1.srv.releng.usw2.mozilla.com --find-links=https://releng-puppet1.srv.releng.mdc1.mozilla.com/python/packages-3.x --trusted-host releng-puppet1.srv.releng.mdc1.mozilla.com --find-links=https://releng-puppet2.srv.releng.mdc1.mozilla.com/python/packages-3.x --trusted-host releng-puppet2.srv.releng.mdc1.mozilla.com --find-links=https://releng-puppet2.srv.releng.mdc2.mozilla.com/python/packages-3.x --trusted-host releng-puppet2.srv.releng.mdc2.mozilla.com --find-links=https://releng-puppet1.srv.releng.mdc2.mozilla.com/python/packages-3.x --trusted-host releng-puppet1.srv.releng.mdc2.mozilla.com --find-links=https://releng-puppet1.srv.releng.use1.mozilla.com/python/packages-3.x --trusted-host releng-puppet1.srv.releng.use1.mozilla.com urllib3==1.24

If there’s a compile issue, we may need to grab a wheel or add system
packages. We may want to delay this update at this time.

If there’s a dependency problem, we may need a new PR that fixes. The
taskcluster tests in the puppet PR may miss this if it involves a
``# pyup: nodownload`` module.

If there’s a configuration problem, hopefully it’s clear by poking
around the machine. If it’s pinned to an env, that may be part of it. I
found a virtualenv that wouldn’t allow upgrading a package because
someone installed the previous version as ``root``, so ``cltbld``
couldn’t update. a ``chown -R cltbld /builds/scriptworker/lib`` fixed
it.

There may be other failure cases; let’s update this list as we find
them.

signing server
--------------

If we update the signing server dependencies, we probably need to
restart all instances. Docs for restarting are
[here](https://mana.mozilla.org/wiki/display/RelEng/Signing#Signing-(Re%29starting).
The host list is
`here <https://mana.mozilla.org/wiki/display/RelEng/Signing#Signing-Hosts>`__.
The list of people who can ssh in is `here
($shortlist) <https://github.com/mozilla-releng/build-puppet/blob/master/manifests/moco-config.pp#L196-L212>`__

Success
=======

When everything puppetizes successfully, we’re good!
