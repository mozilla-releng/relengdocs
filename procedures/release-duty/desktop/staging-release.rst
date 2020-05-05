.. _staging-release:

Run staging releases
~~~~~~~~~~~~~~~~~~~~

Permissions
^^^^^^^^^^^

To do a staging release, you need to be able to push to try, access to the Mozilla VPN, and have staging shipit read/write access.

See the :ref:`production documentation for how to get Shipit and VPN access <release-duty-permissions>`.

How-to
^^^^^^

In order to prepare a smooth ``b1`` and ``RC``, staging releases should 
be run weekly or at least one week before RC week. In order for this to
happen, we're using `staging releases submitted to
try <https://firefox-source-docs.mozilla.org/tools/try/selectors/release.html>`__.

**For central to beta migration**

-  hop on ``central`` repository
-  make sure you're up to date with the tip of the repo
-  ``mach try release --version <future-version.0b1> --migration central-to-beta --tasks release-sim``

**For beta to release migration**

-  hop on ``beta`` repository
-  make sure you're up to date with the tip of the repo
-  ``mach try release --version <future-version.0> --migration beta-to-release --tasks release-sim``

These will create try pushes that look-alike the repos once they are
merged. Once the decision tasks of the newly created CI graphs are
green, staging releases can be created off of them via the
`shipit-staging <https://shipit.staging.mozilla-releng.net/>`__
instance. For how to create a release via Shipit, refer to the
:ref:`production documentation <doing_a_release>`. The same applies to staging,
just ensure you are using the staging instance
(https://shipit.staging.mozilla-releng.net).

One caveat here is the list of partials that needs to be filled-in.
:warning: The partials need to exist in
`S3 <http://ftp.stage.mozaws.net/pub/firefox/releases/>`__ and be valid
releases in `Balrog
staging <https://balrog-admin-static-stage.stage.mozaws.net/>`__.


Once the staging releases are being triggered, it's highly recommended
that at least a comment is being dropped to Sheriffs team
(e.g. ``Aryx``) to let them know these are happening in order to: \*
avoid stepping on each others toes as they may run staging releases as
well \* make sure we're up-to-date to recent patches that they may be
aware of

:warning:
   Allow yourself enough time to wait for these staging releases
   to be completed. Since they are running in ``try``, they have the lowest
   priority even on the staging workers so it usually takes longer for them
   to complete.
