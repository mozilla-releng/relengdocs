
Mobile Releases
===============


Background
----------

QA will test a potential Fennec release and let us know the results. If
the tests all pass, we will have to push the ``apk`` to Google Play.

To do this we create a new task graph to perform all the release
promotion steps.

Prerequisites
-------------

-  VPN Access
-  Ship-it v2 access
-  (Optional, convenient)
   `taskcluster-cli <https://github.com/taskcluster/taskcluster-cli>`__
   set up

When to perform these steps
---------------------------

The release-signoff mailing list will receive a message alerting us that
testing of Fennec has been completed. If the testing is successful, they
will ask us to push the result to the Google Play store.

Below is an example email. The key text to look for will be
``Testing status:GREEN / DONE`` or something similar.

::

   Subject: [mobile] Firefox 58 Beta 5 build 2 - Sign Off of Manual Functional Testing - please push to google play

   Hi all,

   Here are the results for the Fennec 58 Beta 5 build 2.

   Testing status:GREEN / DONE
   *1. Overall build status after testing:* GREEN/OK - No blockers or major
   bugs found

   *2. Recommendation from QE*:  ship to partner's markets
   *3. Manual Testing Summary :*
   *4. New bugs:
   *5. Known Issues:*

Ship
----

Finding the Action Task ID
~~~~~~~~~~~~~~~~~~~~~~~~~~

-  `Find the promote
   graphid <https://github.com/mozilla-releng/releasewarrior-2.0/blob/master/docs/release-promotion/common/find-graphids.md#finding-graphids>`__
   for this release.

Creating the ship graph
~~~~~~~~~~~~~~~~~~~~~~~

-  We will create a new task with the label ‘Action: Release Promotion’
   in the existing on-push graph.
-  This action will create a new ship graph
-  Click on the corresponding phase button in the `Ship-it v2
   UI <https://shipit.mozilla-releng.net/>`__\ .
-  Find the graphid in the Ship-it v2 UI. Every phase is linked to the
   corresponding graph after it’s scheduled.
-  Announce to release-signoff that the release is live
