Merge Duty for major ESR bump
=============================

Intro
-----

This manual describes how to set up a new ESR branch. The same process
can be applied for any branch set up, with slight modifications.

Example tracking bug: `Bug 2046072 - [meta] support ESR153 <https://bugzilla.mozilla.org/show_bug.cgi?id=esr153>`__

General advice
--------------

For in-tree changes, grepping for the old `esrXX` (e.g. `on searchfox
<https://searchfox.org/mozilla-central/search?q=esr153>`__) should be a good
starting point to figure out the necessary updates.  It can also be
useful to compare with the changes from the previous ESR bump.

CI relies on multiple systems, supported by different teams. File bugs in
advance to make sure other teams have enough time to address the task. Since
this is a once-a-year process, there are changes each time, so it's useful to
have some buffer to address unforeseen issues.  Usually starting the whole
process 3 weeks in advance of release builds (4 weeks before the release), gives
enough time to everybody.

The timing is relatively flexible for most tasks, especially early on.  Work
can start as soon as the new ESR major version is known with a reasonable level
of certainty.  Some of the tasks can be done in parallel.

We generally get started early in the nightly cycle corresponding to the new esr
major version.

Pushing to the esr branch
-------------------------

There are several steps in the following list that require you to push to the
esr branch directly. For this, you have to use the `lando CLI <https://github.com/mozilla-conduit/lando-cli>`__

You can install it by doing the following:

.. code-block:: bash

    uv tool install lando-cli

To push a commit to the firefox repository, first navigate to a local clone of it.
You can now do something along the line of this:

.. code-block:: bash

   LANDO_URL="..." LANDO_USER_EMAIL="..." LANDO_HEADLESS_API_TOKEN="..." lando push-merge --lando-repo firefox-esrXX --target-commit $hash --commit-message "Merge beta -> ESRXX"

Until `bug 1971515 <https://bugzilla.mozilla.org/show_bug.cgi?id=1971515>`__ is
fixed, this will say it's going to create a merge commit even when it's a fast
forward merge. Do not omit the `--commit-message` parameter or it will take
the current HEAD of your repository as the commit to push and ignore `--target-commit`.

Task list and known dependencies
--------------------------------

0. File a meta bug: support ESRXX (alias esrXX)

1. Add new ESR to mozilla-version, and make a new release

2. Add new ESR to scriptworker constants, and make a new release

3. After steps 1 and 2, pull new mozilla-version and scriptworker releases in
   scriptworker-scripts, shipit, `ronin_puppet
   <https://github.com/mozilla-releng/scriptworker-scripts/wiki/Mac-Signers-Maintenance#deploying-scriptworker-updates>`__,
   anywhere else they're used.

4. Set up new rules in balrog staging and production instances:

   - a rule with alias `firefox-esrXX-localtest` on the `esr-localtest*` channel
   - a rule with alias `firefox-esrXX-cdntest` on the `esr-cdntest*` channel
   - a rule with alias `esrXX` on the `esr` channel

   The rules can initially point at the `No-Update` mapping and are then updated by automation.
   Rules on the `esr-localtest-next` and `esr-cdntest-next` channels should be
   adjusted so that updates to the new ESR are served (sometimes with a watershed
   on the previous ESR, depending on app requirements; otherwise the rules for the
   previous ESR can be changed to no longer apply to the `-next` channels, i.e. remove the wildcard).
   Each `esrXX` rule's `Version` field should be set to `<XY.0` where `XY == XX+1`.

   Before the first release from the new ESR branch, the
   `release-bouncer-aliases` task on the previous ESR branch needs to be updated
   to not touch the `firefox-esr-next-*` aliases, to avoid issues like `bug
   1786507 <https://bugzilla.mozilla.org/show_bug.cgi?id=1786507>`__.

5. After 4, add esrXX support in `gecko_taskgraph`.

6. After 5, run a ESRXX staging release to identify release automation
   failures (then fix and repeat as necessary). (`./mach try release
   --version XX.0esr --migration main-to-beta --migration beta-to-release
   --migration release-to-esr --disable-pgo`).

7. Add staging-firefox-esrXX to lando

8. After 5 and 7, test the release-to-esr merge automation task on try

9. After 5, once XX becomes the current beta, run a beta as esr simulation to
   identify permanent build and test failures. (`./mach try release
   --disable-pgo -v XX.0esr --migration beta-to-release --migration
   release-to-esr --tasks release-sim`). Don't hesitate to ask sheriffs for
   help with classification of tests failures.

10. Create the mozilla-esrXX and comm-esrXX mercurial repositories, cloned from {mozilla,comm}-beta.

11. After 10, create the esrXX branch in the firefox github repo, at the same commit as its mercurial counterpart.

12. Add esrXX to treestatus / lando

13. After step 12 (and after beta has had a new push), push the tip of
    beta to esrXX.  This ensures mozilla-esrXX's pushlog is not
    empty.

14. After 13, add the mozilla-esrXX project to fxci-config

15. After 14 (and after beta has had a new push), push the tip of mozilla-beta to
    mozilla-esrXX (the goal is to get a first set of tasks, so pick a
    non-DONTBUILD push :) )

16. After 11, add esrXX to `l10n automation <https://github.com/mozilla-l10n/firefox-l10n-source/blob/main/.github/update-config.json>`__ configuration

17. Add esrXX to treeherder

18. After 15, add esrXX to searchfox

19. Add esrXX to bugherder

20. `File a GitHub issue <https://github.com/mozilla/code-review/issues/new>`__
    asking for mozilla-esrXX to be added to mozilla/code-review

21. After 20, `file a bug <https://bugzilla.mozilla.org/enter_bug.cgi?product=Conduit&component=Phabricator>`__
    asking for the esrXX repository to be added to Phabricator, as
    mozilla-esrXX, tagged for uplifts, and hooked up to code-review-bot

22. Add esrXX to the `legacy approval mapping for bmo.
    <https://github.com/mozilla-bteam/bmo/blob/ed603350fcf9822672555d1822f2d9f51db305e5/extensions/PhabBugz/lib/Util.pm#L46-L52>`__

23. Add esrXX status/tracking/approval flags to bugzilla (typically around RC
    week; they can be added earlier but should be kept disabled until release
    managers give a go ahead)

24. Add mozilla-esrXX and comm-esrXX to the shipit frontend, pointing at the
    previous major ESR version for partials
    (alternativeBranch/alternativeRepo), set ESR_NEXT to XX in the backend
    config, and deploy to production.

25. After the beta-to-release merge (RC week for XX), push the
    mozilla-release tip to mozilla-esrXX, then run the release-to-esr migration
    (which sets the display version number).

26. After 25, turn on the periodic updates cron jobs.

27. After the first esrXX release, enable the cron-bouncer-check job on
    mozilla-esrXX (maybe trigger the hook manually first)

28. After the last scheduled release from the previous ESR branch, and before
    the first standalone esrXX release (typically XX.5.0), make esrXX not
    next-esr: update the release-bouncer-aliases task to update the main esr
    bouncer aliases, and run update-verify from older major versions (adjust
    last-manifest)

29. Before gtb for XX.5.0 (beginning of RC week for XX+5), update balrog rules
    on esr-localtest and esr-cdntest to allow updates to esrXX; check rules on
    the release channel, and check with release management for any necessary
    watershed and/or desupport rules.

30. At XX.5.0 release time, update the rules on balrog's esr channel (similar to 26).

31. Around the same time, update shipit's `CURRENT_ESR` and `ESR_NEXT` config
    variables, and rebuild product-details.

32. Shortly after the XX.5.0 release, update the cron-bouncer-check task's
    config on esrXX to look at `FIREFOX_ESR` instead of `FIREFOX_ESR_NEXT`.

33. Some time later (maybe soon after the XX.5.0 release to avoid forgetting),
    stop running update-verify-next on esrXX, stop updating the esr-next
    aliases, and remove them from bouncer check.

34. Close the meta bug and have some tea. :)
