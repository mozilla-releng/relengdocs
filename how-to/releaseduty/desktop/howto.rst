Desktop Releases
================

For an overview of how to do a release end-to-end, see :ref:`How To Do A Release <doing_a_release>`

Managing Different Types of Releases
------------------------------------

Betas and Devedition
^^^^^^^^^^^^^^^^^^^^

Aside from the first beta and devedition of a new cycle (e.g. 77.0beta1), Beta and
Devedition releases are done automatically. No human or manual intervention is
required. The releases are created via Taskcluster Cron, 3 times a week (Mon,
Wed, and Fri), at 03:00 UTC. These releases are still driven through Shipit but
automation creates and triggers the ship phase via the Shipit API.

As releaseduty, you are required to ensure that each beta and devedition
release ships without bustage. In other words, ensure that the ship phase in
Shipit has 100% green tasks in the associated Taskcluster graph. You are not
expected to actively monitor the graph, particularly if 03:00-06:00 UTC is not
within our range of your normal working hours. That said, you are expected to
confirm the release is unblocked and all green as you start or finish your day.

Sheriff support: Sheriffs actively monitor releases so they will often
discover, rerun intermittents, and escalate to #releaseduty on Matrix if a
release is stuck.

Release Candidate(RC) week and Beta 1: beta1 releases are initiated manually by
Release Management. Automatic betas can be disabled via Shipit. See Shipit
documentation (TODO add link and docs) for disabling and re-enabling automatic
betas via the Shipit UI. When we create a Release Candidate (see below), we
close mozilla-beta via Treestatus which stops developers from landing patches
on the Beta based repository. We keep it closed for one week and Relman disable
automatic betas from triggering. After one week, Release Management will
re-open mozilla-beta, trigger the new cycle's first Beta release (beta1)
manually via Shipit, and then re-enable automatic betas so that Beta (and
Devedition) based releases will start shipping automatically again.

Balrog signoffs: release updates for Betas and Devedition do not require human
signoff in Balrog.

Release Candidates
^^^^^^^^^^^^^^^^^^

Over the course of 1 week (the last week of each cycle), Release Management
create a new Release Candidate (RC) release once a cycle. e.g. 76.0. This
release is created manually in Shipit via Release Management. It is comprised
of 4 phases: promote, ship on beta, push, and ship on release. Each phase is
triggered by Release Management when they are ready. Even though this release
is intended for the "release" channel,  we ship it to "beta" channel users to
test it with the beta population. Often we will have many RC releases in a week
and ship each one to the beta population. The reason this does not cause update
conflicts to beta users is because we freeze actual beta releases during RC
week. See above Beta section. So beta users prior to receiving say 76.0, will
be on <= 76.0betaN. Where N is the last beta we released. 76.0 itself is
basically the same, plus maybe a few uplifts, as 76.0betaN. While we may have
many RC releases that ship to beta users each time, we will only ship one RC to
release based users. The final RC release.

Release management initiate and trigger each RC phase via Shipit. Releng
releaseduty is only expected to ensure the integrity of the release graphs and
resolve issues as they come up.

Once we ship to "release" based users, releaseduty is required to signoff in
Balrog. Balrog requires one person  from relman and one person from releng to
signoff on any changes to updates. See documentation on how to signoff in
Balrog here (TODO add URL or docs)

ESR and Dot Releases
^^^^^^^^^^^^^^^^^^^^

ESR and dot releases releases are similarly all initiated and triggered by
Release Management. Dot releases are releases on the release channel that are
not full new major version based changes. e.g. 76.0.1 vs 76.0. In other words,
they are not RC based releases. releaseduty is expected to monitor the graphs
and ensure all tasks are green. When shipped, releaseduty is required to
signoff in Balrog.
