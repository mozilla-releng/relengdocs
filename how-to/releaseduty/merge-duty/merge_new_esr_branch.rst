Merge Duty for major ESR bump
=============================

Intro
-----

This manual describes how to set up a new ESR branch. The same process
can be applied for any branch set up, with slight modifications.

Example tracking bug: `Bug 1835641 - [meta] support ESR115 <https://bugzilla.mozilla.org/show_bug.cgi?id=esr115>`__

General advice
--------------

For in-tree changes, grepping for the old `esrXX` (e.g. `on searchfox
<https://searchfox.org/mozilla-central/search?q=esr115>`__) should be a good
starting point to figure out the necessary updates.  It can also be
useful to compare with the changes from the previous ESR bump.

We generally get started early in the nightly cycle corresponding to the new
esr major version.  Some of the tasks can be done in parallel. The timing is
relatively flexible for most tasks, especially early on.  Work can start as
soon as the new ESR major version is known with a reasonable level of
certainty.

CI relies on multiple systems, supported by different teams. File bugs
in advance to make sure other teams have enough time to address the
issue. Usually starting the whole process 2 weeks in advance of release
builds (3 weeks before the release), gives enough time to everybody.

Task list and known dependencies
--------------------------------

0. File a meta bug: support ESRXX (alias esrXX)

1. Add new ESR to mozilla-version, and make a new release

2. Add new ESR to scriptworker constants, and make a new release

3. After steps 1 and 2, pull new mozilla-version and scriptworker releases in
   scriptworker-scripts, shipit, anywhere else they're used.

4. Set up new rules in balrog staging and production instances:

   - a rule with alias `firefox-esrXX-localtest` on the `esr-localtest*` channel
   - a rule with alias `firefox-esrXX-cdntest` on the `esr-cdntest*` channel
   - a rule with alias `esrXX` on the `esr` channel

   The rules can initially point at the `No-Update` mapping and are then updated by automation.
   Rules on the `esr-localtest-next` and `esr-cdntest-next` channels should be
   adjusted so that updates to the new ESR are served (sometimes with a watershed
   on the previous ESR, depending on app requirements; otherwise the rules for the
   previous ESR can be changed to no longer apply to the `-next` channels).
   Each `esrXX` rule's `Version` field should be set to `<XY.0` where `XY == XX+1`.

   Before the first release from the new ESR branch, the
   `release-bouncer-aliases` task on the previous ESR branch needs to be updated
   to not touch the `firefox-esr-next-*` aliases, to avoid issues like `bug
   1786507 <https://bugzilla.mozilla.org/show_bug.cgi?id=1786507>`__.

5. Add esrXX support in `gecko_taskgraph`

6. Create the mozilla-esrXX and comm-esrXX mercurial repositories.

7. Add esrXX to the gecko-dev github repo.

8. After step 6 (and after beta has had a new push), push the tip of
   mozilla-beta to mozilla-esrXX.  This ensures mozilla-esrXX's pushlog is not
   empty.

9. After 8, add the mozilla-esrXX project to fxci-config

10. After 9 (and after beta has had a new push), push the tip of mozilla-beta to
    mozilla-esrXX (the goal is to get a first set of tasks, so pick a
    non-DONTBUILD push :) )

11. After 6, add esrXX to cross-channel configuration

12. Add esrXX to treeherder

13. Add esrXX to treestatus / lando

14. After 10, add esrXX to searchfox

15. Add esrXX to bugherder

16. `File a GitHub issue <https://github.com/mozilla/code-review/issues/new>`__
    asking for mozilla-esrXX to be added to mozilla/code-review

17. After 16, `file a bug <https://bugzilla.mozilla.org/enter_bug.cgi?product=Conduit&component=Phabricator>`__
    asking for the esrXX repository to be added to Phabricator, as
    mozilla-esrXX, tagged for uplifts, and hooked up to code-review-bot

18. Run a beta as esr simulation to identify permanent build and test failures

19. Run a ESRXX staging release to identify release automation failures (then
    fix and repeat as necessary)

20. Add esrXX status/tracking/approval flags to bugzilla (typically around RC
    week; they can be added earlier but should be kept disabled until release
    managers give a go ahead)

21. Add mozilla-esrXX and comm-esrXX to the shipit frontend, pointing at the
    previous major ESR version for partials
    (alternativeBranch/alternativeRepo), set ESR_NEXT to XX in the backend
    config, and deploy to production.

22. After the beta-to-release merge (start of RC week for XX), push the
    mozilla-release tip to mozilla-esrXX, then run the release-to-esr migration
    (which sets the display version number)

23. After the first esrXX release, enable the cron-bouncer-check job on
    mozilla-esrXX (maybe trigger the hook manually first)

24. After the last scheduled release from the previous ESR branch, and before
    the first standalone esrXX release (typically XX.3.0), make esrXX not
    next-esr: update the release-bouncer-aliases task to update the main esr
    bouncer aliases, and run update-verify from older major versions (adjust
    last-manifest)

25. Before gtb for XX.3.0 (beginning of RC week for XX+3), update balrog rules
    on esr-localtest and esr-cdntest to allow updates to esrXX; check rules on
    the release channel, and check with release management for any necessary
    watershed and/or desupport rules.

26. At XX.3.0 release time, update the rules on balrog's esr channel (similar to 22).

27. Around the same time, update shipit's `CURRENT_ESR` and `ESR_NEXT` config
    variables, and rebuild product-details.

28. Shortly after the XX.3.0 release, update the cron-bouncer-check task's
    config on esrXX to look at `FIREFOX_ESR` instead of `FIREFOX_ESR_NEXT`.

29. Some time later (maybe soon after the XX.3.0 release to avoid forgetting),
    stop running update-verify-next on esrXX, and stop updating the esr-next
    aliases

30. Close the meta bug and have some tea. :)
