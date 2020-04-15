
Mobile Release Candidates
=========================

Background
----------

For Fennec RCs, we roll out to Google Play at 5% until we know if it’s a
good RC (via the ``ship_fennec_rc`` relpro flavor).

At that point, we run the ``ship_fennec`` graph to mark it as shipped.

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

   Subject: [mobile] Firefox 60 RC 5 build 2 - Sign Off of Manual Functional Testing - please push to google play

   Hi all,

   Here are the results for the Fennec 60 RC 5 build 2.

   Testing status:GREEN / DONE
   *1. Overall build status after testing:* GREEN/OK - No blockers or major
   bugs found

   *2. Recommendation from QE*:  ship to partner's markets
   *3. Manual Testing Summary :*
   *4. New bugs:
   *5. Known Issues:*

ship-rc
-------

Creating the RC ship graph
~~~~~~~~~~~~~~~~~~~~~~~~~~

-  We will create a new task with the label ‘Action: Release Promotion’
   in the existing on-push graph.
-  This action will create a new ship-rc graph
-  Click on the corresponding phase button in the `Ship-it v2
   UI <https://shipit.mozilla-releng.net/>`__.
-  Find the graphid in the Ship-it v2 UI. Every phase is linked to the
   corresponding graph after it’s scheduled.
-  Announce to release-signoff that the release is live

ship
----

Creating the ship graph
~~~~~~~~~~~~~~~~~~~~~~~

-  We will create a new task with the label ‘Action: Release Promotion’
   in the existing on-push graph.
-  This action will create a new ship graph
-  Click on the corresponding phase button in the `Ship-it v2
   UI <https://shipit.mozilla-releng.net/>`__.
-  Find the graphid in the Ship-it v2 UI. Every phase is linked to the
   corresponding graph after it’s scheduled.
-  Announce to release-signoff that the release is live
