Merge Duty for major ESR bump
=============================

Intro
-----

This manual describes how to set up a new ESR branch. The same process
can be applied for any branch set up, with slight modifications.

Example tracking bug: `Bug 1717527 - tracking bug for build and release
of Firefox
91.0esr <https://bugzilla.mozilla.org/show_bug.cgi?id=1717527>`__

Internal changes
----------------

External systems
----------------

CI relies on multiple systems, supported by different teams. File bugs
in advance to make sure other teams have enough time to address the
issue. Usually starting the whole process 2 weeks in advance of release
builds (3 weeks before the release), gives enough time to everybody.

Tasks
-----

for the `tracking bug <https://bugzilla.mozilla.org/show_bug.cgi?id=1717527>`__
look at each bug in the tree and see if it is needed in the next ESR.  Most likely it will be.

Odd problems
------------

mozilla-version needed an `update <https://github.com/mozilla-releng/mozilla-version/commit/3d9f3361505fbb485ea6103c2be6e2a8a4d41ec1>`__.
 * remember to push shipit changes that contain mozilla-version update to production branch, don't leave on master only
 * remember to update `treescript <https://github.com/mozilla-releng/scriptworker-scripts/commit/d0ffb3c1c0095798c50e0f126e47280404b720ed>`__
 * remember to merge scriptworker-script (treescript) changes to production and let the ci-change bot complete

UVNEXT* tasks (update verify next) will fail (run in promote phase) unless proper balrog (esr-localtest-next) rule exists


Merge
-----

Merge beta to release
~~~~~~~~~~~~~~~~~~~~~

1. Run the ``m-r -> m-esrXX`` no-op trial run:

.. code:: yaml

   force-dry-run: true
   behavior: release-to-esr
   push: true

2. The diff for ``esrXX`` should be fairly similar to 
   `this <https://hg.mozilla.org/releases/mozilla-esr91/rev/075b0b573ba8b73514cb652d114fd1c00983fd0d>`__,
3. Submit a new task with ``force-dry-run`` set to false:

.. code:: yaml

   force-dry-run: false
   behavior: release-to-esr
   push: true

:warning:
   It's not unlikely for the push to take between 10-20 minutes to complete.

Release builds
--------------

Make sure to run a staging release.

Update this documentation
-------------------------

Keep this documentation up to date.

Ship it!
--------

Close the bug and have some tea. :)
