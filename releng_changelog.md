# Releng Changelog

Every time a new releaseduty cycle begins, new RelEng people are (re)ramping up. To ease the transition, we're keeping this CHANGELOG that should trace all the tools/productivity/infrastructure changes. This includes high-level changes and should come into compliance with the rest of the documentation.

This page best serves the people that have previously been into the releaseduty cycle. Starting from the baseline, people coming back after `N` cycles can ramp up incrementally with the latest changes.

_**As releaseduty squirrels are the ones with the best context when it comes to releases, they are the ones to edit this page and amend it accordingly. Keep in mind that changes should be in compliance with the other pieces of documentation.**_

### During 96.0 >= 2021-11-01
#### Changed
-

### During 95.0 >= 2021-10-04
#### Changed
- focus-android releases switched to taskgraph
- new firefox desktop balrog watershed

### During 82.0 >= 2020-09-21
#### Changed
- partner attribution configs landed
- balrog v2 submission
- ESR68 EOL
- central-to-beta merges should automatically l10n-bump

### During 81.0 >= 2020-08-24
#### Changed
- L10n bumper will look at the hg pushlog for the default revision, rather than Elmo. If we need to pin a previous revision due to bustage, land a change updating the revision and changing `pin` to `true` for that locale.
- ESR68 l10n bumper disabled.
- partner builds moved from b8 to b5 to adjust for shorter release cycles
- partner attributions landed

### During 80.0 >= 2020-07-27
#### Changed
- Lots of accounts disabled; watch for fallout!

### During 75.0 >= 2020-04-06
#### Changed
- Changelog moved to [rtd](https://moz-releng-docs.readthedocs.io/en/latest/releng_changelog.html)
- Mac Notarization is now single-zip instead of multi-account due to [bug 1620697](https://bugzilla.mozilla.org/show_bug.cgi?id=1620697). This may slow down the success case by a few minutes, but reduce or remove the multi-hour manual-intervention failure case.

#### Fixed
- Scriptworker now catches a number of `asyncio.TimeoutError`s, and should be more robust.

### During 74.0 >= 2020-03-10
#### Added
- added support for shipping Firefox Flatpaks to [Flathub](https://flathub.org/apps/details/org.mozilla.firefox)

### During 73.0 >= 2020-02-10
#### Changed
- py38 rollout for scriptworkers, tooltool, balrog, and other release services
- aws -> gcp, then back again, for tier 1 workers
- mac 3-tier notarization

### During 71.0 >= 2019-10-14
#### Changed
- (still-in-progress) signing servers are being shut down. we've already stopped using them, however
- mergeduty processed is back to two stages like it used to be before Quantum: beta -> release in the first iteration
while central -> beta and bumping central in the second week
- l10n bumper for central is moving to taskcluster cron shortly; will uplift to beta and esr68 later
- switched to GCP scriptworkers in all gecko trees (including esr68)
- after TCW of 9th Nov, switched to GCP scriptworkers in `comm` repos too, but also Github mobile projects
- secrets are now managed in `sops`, no longer in `hiera`
- decommissioning of the AWS infrastructure
- treescript has been refactored
- scriptworker-scripts docker images now mount the repo at `/app` instead of the script (we may revisit this to lower disk usage)
- mergeduty process change for upcoming automated betas. tl;dr - no longer Devedition b1 and b2 during RC week. central merges to beta a week later

### During 69.0 >= 2019-05-13
#### Changed
- mac signing now happens on the mac notarization pool.
- mac nightly and release builds are now notarized as well as signed.
- mac signing tasks also create pkg installers

### During 67.0 >= 2019-03-11
#### Changed
- update & final verify will check SSL certificates of Balrog, archive.m.o etc
- the release promotion action is now a hook.
- chain of trust no longer uses gpg to create and verify signatures.

### During 66.0 >= 2019-01-30
#### Changed
- scriptworker 22 now signs and verifies ed25519 signatures; gpg signatures are deprecated.
- partner repacks are now enabled on ESR60
- adding list of whatsnewpage locales in-tree is now part of mergeduty
- removed thunderbird docs. thunderbird is now managed by thunderbird team and they have support for shipit v2

### During 64.0 >= 2018-10-15
#### Changed
- MARs are now signed via autograph (hashes only)
- Mergeduty tasks are now tracked in [Trello](https://trello.com/b/AyyFAEbS/mergeduty-tasks)
- Releaseduty now assists CIDuty with [puppet pyup PRs](https://github.com/mozilla-releng/releasewarrior-2.0/blob/master/docs/misc-operations/puppet-pyup.md) once per week

### During 63.0 >= 2018-09-05
#### Added
- added 6 new mac signing servers

#### Changed
- switched to ship-it v2
- reduced mac signing concurrency from 4 to 2 to reduce server churn

### During 62.0 >= 2018-06-26

#### Changed
- switched to Ship-it v2 for beta releases

#### Added
- releasewarrior local automation to add WNP

### During 61.0 >= 2018-05-09

#### Added
- added partner off-cycle support + docs
- widevine docs

#### Changed
- update verify only blocks on required platforms to start (eg: win32 update verify only blocks on win32 beetmover and balrog)
- python 2.7.15 rollout to a portion of our infra
- python 3.6.5 rollout completed to our scriptworkers
- update verify no longer fails on expected differences, but will fail on any files found only in source or target; [bug 1461490](https://bugzilla.mozilla.org/show_bug.cgi?id=1461490)

### During 60.0 >= 2018-03-13

#### Added
- releaseduty now responsible for periodic file update approvals in phabricator. Change [this line](https://dxr.mozilla.org/mozilla-central/source/taskcluster/ci/repo-update/kind.yml#34) to update those responsible.
- added `esr52-latest*` bouncer aliases
- added `firefox-esr-next-*` bouncer aliases
- added esr60 support
- rerun action task in Treeherder - hopefully will help avoid duplicate reruns
- KEY file to releases directory in [bug 1446816](https://bugzilla.mozilla.org/show_bug.cgi?id=1446816) for >=60.0b11
- added addonscript for langpack pushing to amo

#### Changed
- re-added source tarball for >=60.0b6
- updated scriptworkers to share more client code
- update verify now fails on any differences, and creates a summary log for >=60.0b8. additional documentation on [how to interpret failures](https://github.com/mozilla-releng/releasewarrior-2.0/blob/master/docs/misc-operations/analyze-update-verify-logs.md) are available.
- split snap repackage and push task in [bug 1447263](https://bugzilla.mozilla.org/show_bug.cgi?id=1447263)
- updated rr3 add partner configs for fx60+
- tc partner repacks!
- split esr52 and esr60 templates

#### Fixed
- fixed beta+fennec bouncer aliases
- push-apk-breakpoint removed in [bug 1432817](https://bugzilla.mozilla.org/show_bug.cgi?id=1432817)

### During 59.0 >= 2018-01-24

#### Added
- we track all major changes in this newly added CHANGELOG
- separate RC docs for both Fennec and Firefox
- new-style WNP setup, [as documented](https://github.com/mozilla-releng/releasewarrior-2.0/blob/master/docs/release-promotion/desktop/howto-rc.md#add-a-whats-new-page-to-a-firefox-rc).
- we now have support for snaps in `release` channel

#### Changed
- old release promotion based on [releasetasks](https://github.com/mozilla/releasetasks/) is dead. Everything is in-tree scheduled now. Changes are riding the trains.
- all releaseduty related documentation has been moved out of the wiki under [warrior's](https://github.com/mozilla-releng/releasewarrior-2.0) `docs` subfolder.
- use `release graphid` to enter graphids, rather than editing the .json manually.
- in-tree release notifications going away in favor of native taskcluster notifications. pulse-notify is to be retired whenever we kill esr52
- Balrog toplevel submission and release scheduling now happens in balrog scriptworker for Fx60+.

### During 58.0 >= 2017-11-15

#### Added
- the use of the new [releasewarrior](https://github.com/mozilla-releng/releasewarrior-2.0)

#### Changed
- old how-tos are now gathered under one roof in releasewarrior-2.0/old-howtos[releasewarrior-2.0/old-how-tos](https://github.com/mozilla-releng/releasewarrior-2.0/tree/master/old-how-tos) but they are gradually being migrated to the [wiki](https://github.com/mozilla-releng/releasewarrior-2.0/wiki) which becomes the single source of truth
- authentication method for [taskcluster-cli](https://github.com/taskcluster/taskcluster-cli#installation) changed. If you are upgrading from an older version of taskcluster-cli, you may have to remove the `${HOME}/.config/taskcluster.yml` file to work with the new authentication method.

#### Removed
- dropped support for old [releasewarrior](https://github.com/mozilla/releasewarrior/)
- dropped the need for QE signoffs in Balrog

### During 57.0 >= 2017-09-27

#### Added
- a merge day instance has been added to ease the handover during mergedays but also for speed and reliability. More on this [here](https://github.com/mozilla-releng/releasewarrior-2.0/wiki/Merge-Duty). When connecting  to the merge day instance, keep in mind to ensure its environment is clean and ready for use
- simplified documentation for mid-betas and release checklists. If not already, duplicate an existing sheet in this [google docs checklist](https://docs.google.com/spreadsheets/d/1hhYtmyLc0GEk_NaK45KjRvhyppw7s7YSpC9xudaQZgo/edit#gid=1158959417) and clear out the status that was carried over from the previous release.

#### Changed
- mergeduty dates shifted. We now merge `beta` to `release` and `cetral` to `beta` in the same day, keeping a relbranch for `beta` and hold `central` from version bump until before the release.
- because of 57 and the aforementioned mergeduty change, *the exception becomes rule* so that for each new beta cycle X, we have X.0b1 and X.b2 **just** for `Devedition`, while `Firefox` starts at X.b3

#### Removed
- dropped support for [tctalker](https://github.com/mozilla/tctalker) and solely rely on [taskcluster-cli](https://github.com/taskcluster/taskcluster-cli). More on its installation [here](https://github.com/taskcluster/taskcluster-cli#installation)

### During 56.0 >= 2017-08-09

#### Added
- releaseduty now checks on status of central nightlies when not undertaking other duties
- releaseduty now handles signing of arbitrary .apk's as requested by MoCo teams (Klar/Focus, Rocket)

#### Changed
- release-drivers mailing list is no longer used for signoffs/gtb's, please subscribe to release-signoffs@
- QE will now send an explicit GO for DevEdition Beta's to be pushed live, usually in the same e-mail as the GO for Beta

#### Removed
- Fennec single locales no longer shipped
