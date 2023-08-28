Analyze Update Verify Logs
==========================

When?
-----

When update verify tasks fail it is your responsibility as releaseduty
to analyze them and determine whether or not any action needs to be
taken for any differences found.

How?
----

Update verify tasks that have failed usually have a ``diff-summary.log``
in their artifacts. This file shows you all of the differences found for
each update tested. In the diffs, ``source`` is an older version Firefox
that a MAR file from the current release has been applied to, and
``target`` is the full installer for the current release.

Here's an example of a very alarming difference:

::

   Found diffs for complete update from https://aus5.mozilla.org/update/3/Firefox/59.0/20180215111455/WINNT_x86-msvc/en-US/beta-localtest/default/default/default/update.xml?force=1

   Files source/bin/xul.dll and target/bin/xul.dll differ

In the above log, ``xul.dll`` is shown to be different between an
applied MAR and a full installer. If we were to ship a release with a
difference like this, partial MARs would fail to apply for many users in
the *next* release. Usually a case like this represents an issue in the
build system or release automation, and requires a rebuild. If you're
not sure how to proceed, ask for help.

If no ``diff-summary.log`` is attached to the Task something more
serious went wrong. You will need to have a look at live.log to
investigate.

Known differences
-----------------

There are no known cases where diffs are expected, so all task failures
should be checked carefully.

See `bug
1461490 <https://bugzilla.mozilla.org/show_bug.cgi?id=1461490>`__ for
the implementation of transforms to resolve expected differences.
