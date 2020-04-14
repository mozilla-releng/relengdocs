Release Promotion
=================


Contents:

.. toctree::
    :maxdepth: 1
    :glob:

    desktop/*
    mobile/*
    common/*


Requirements
------------

-  All steps followed from Day1 documentation
-  Ability to run the ``release`` command and find the task group
   inspector URLs for releases in flight.

Actions for Desktop related releases
------------------------------------

Summary
~~~~~~~

1. Push artifacts to releases directory (also known as mirrors / CDN)
2. Obtain sign-offs for changes
3. Publish the release
4. Post-release steps

Instructions vary slightly depending on the type of release, so please
be careful when following the instructions.

Notes and Background
~~~~~~~~~~~~~~~~~~~~

-  ``-cdntest`` and ``-localtest`` channels serve releases from the
   releases directory (mirrors or CDN) or candidates directory depending
   on the release and channel. They are testing channels used before we
   serve from the *real* update channel, but they use the *actual files*
   that will be served once a release is published.
-  We should notify release-signoff once updates are available on the
   ${branch}-{cdntest,localtest} channel because we don’t have
   taskcluster email notifications yet.

Hand Off
~~~~~~~~

If a scheduled release has not completed its Promote graph (and Push
graph if devedition/beta) prior releaseduty signing off. An explicit
hand-off describing describing release state should be sent to individual
folks in releng that are scheduled to come online next or will be around
for a while after you. #mozbuild in Slack is best. A release@m.c email
would be useful too.

Escalation
~~~~~~~~~~

If a release is blocked. The normal flow is to:

1. confirm issue
2. determine what service, task kind, infrastructure, or external
   dependency is involved
3. file a ticket
4. determine which team(s) and person(s) should be escalated.

   a. Searching phonebook is useful for org and ownership charts.
   b. bugzilla and github history
   c. source code history

5. escalate in the appropriate Slack and IRC channel(s). At a minimum,
   #releaseduy@irc.
6. determine who is available to help based on above. What hours they
   work, who is their manager, etc
7. ask for help if you can’t determine the above.

Good resources within releng:

-  general release configuration (taskgraph): tomprince/callek
-  scopes / ciadmin: tomprince/mtabara
-  chainoftrust (cot): aki
-  scriptworker (general): aki/jlorenzo
-  beetmoverscript / bouncer / artifact related: mtabara
-  signing / signingscript / autograph: aki/catlee
-  balrog / balrogscript / updates related: bhearsum/nthomas
-  l10n / treescript / addonscript: callek
-  pushapkscript / mozapkpublisher: jlorenzo/mhentges
-  shipit / shipitscript: rail/garbas
