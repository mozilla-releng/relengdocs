Ship RC Firefox releases
========================

Requirements
------------

-  taskcluster-cli installed
-  `Ship-it v2 <https://shipit.mozilla-releng.net/>`__ access

Differences between Firefox RC and non-RC
-----------------------------------------

-  the ``promote`` action will be named ``promote_firefox_rc`` instead
   of ``promote_firefox``

-  there will be an action in between ``promote`` and ``push``. This is
   ``ship_firefox_rc``. The relpro flavors, in order, will be:

   1. ``promote_firefox_rc``
   2. ``ship_firefox_rc``
   3. ``push_firefox``
   4. ``ship_firefox``

   We may repeat the first two several times if there are issues we
   don’t want to ship the real release with.

ship-rc
-------

How
~~~

-  Click on the corresponding phase button in the `Ship-it v2
   UI <https://shipit.mozilla-releng.net/>`__.

-  Find the graphid in the Ship-it v2 UI. Every phase is linked to the
   corresponding graph after it’s scheduled.

push
----



How
~~~

-  Click on the corresponding phase button in the `Ship-it v2
   UI <https://shipit.mozilla-releng.net/>`__.

-  Find the graphid in the Ship-it v2 UI. Every phase is linked to the
   corresponding graph after it’s scheduled.

ship
----

Background
~~~~~~~~~~

The ``ship`` phase should be triggered when the release is signed off.
It runs the ``update bouncer aliases``, ``mark as shipped``, and
``bump version`` tasks.

When
~~~~

An email will arrive to the release-signoff mailing list asking for a
release to be pushed to the appropriate channel, such as ‘release’ for
major releases, ‘beta’ for betas, and so on.

Examples -
``[desktop] Please push Firefox 57.0 (build#4) to the release channel (25%)``



How
~~~

-  Click on the corresponding phase button in the `Ship-it v2
   UI <https://shipit.mozilla-releng.net/>`__.

-  Find the graphid in the Ship-it v2 UI. Every phase is linked to the
   corresponding graph after it’s scheduled.

-  Announce to release-signoff that the release is live

Obtain sign-offs for changes
----------------------------



Background
~~~~~~~~~~

To guard against bad actors and compromised credentials we require that
any changes to primary release channels (beta, release, ESR) in Balrog
are signed off by at least two people.



When
~~~~

After the scheduled change has been created by the “updates” task, and
prior to the desired release publish time



How
~~~

-  In context of the other rules, eg

   -  Firefox release:
      https://aus4-admin.mozilla.org/rules?product=Firefox&channel=release
   -  Firefox beta:
      https://aus4-admin.mozilla.org/rules?product=Firefox&channel=beta
   -  DevEdition:
      https://aus4-admin.mozilla.org/rules?product=Firefox&channel=aurora

-  Or using the Balrog Scheduled Changes UI:
   https://aus4-admin.mozilla.org/rules/scheduled_changes

Further details and examples can be found on the [[Balrog page|Balrog
and Scheduled Changes]]
