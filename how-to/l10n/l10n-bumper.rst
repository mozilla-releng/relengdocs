.. _l10n-bumper:

L10n-Bumper
===========

L10n-bumper is a cron process in mozilla-central and mozilla-beta that we use to pin the latest revisions of the `localized string repos <https://hg.mozilla.org/l10n-central/>`_ in Gecko.

L10n repacks and other l10n tasks use the bumped file, `l10n-changesets.json`_, as their input configuration.

How to adjust l10n-bumper timing + frequency
--------------------------------------------

The timing of the l10n-bumper cron tasks are specified in `.cron.yml <https://hg.mozilla.org/mozilla-central/file/f788858ac268c25b4bc573d4a2642df44af22daa/.cron.yml#l274>`_. Note, we intentionally scheduled these to have enough time for the l10n-bumper-triggered build tasks to complete before nightlies and daily betas trigger.

.. _l10n_bumper_platform_locale_change:

How to change the set of platforms or locales in l10n-bumper
------------------------------------------------------------

The l10n bump configs are in the `kind.yml <https://hg.mozilla.org/mozilla-central/file/f788858ac268c25b4bc573d4a2642df44af22daa/taskcluster/ci/l10n-bump/kind.yml#l31>`_. Our platform configs are explicitly listed.

The ``path`` specifies which locales file we use.
Beta currently uses `browser/locales/shipped-locales <https://hg.mozilla.org/releases/mozilla-beta/file/32ea082794194628fafcaae84eedd9e0923f939c/browser/locales/shipped-locales>`_ to specify the locales we ship on beta (and subsequently release and ESR).

Central currently uses `browser/locales/all-locales <https://hg.mozilla.org/mozilla-central/file/f788858ac268c25b4bc573d4a2642df44af22daa/browser/locales/all-locales>`_ to specify the locales we ship in nightly. The locales list in ``shipped-locales`` should be a subset of ``all-locales``.

How to pin an l10n revision
---------------------------

If localizers have landed a change in an `l10n repo`_ that breaks something, it may be necessary to pin an l10n revision.

Go to `l10n-changesets.json`_ in Central or Beta, as appropriate. Find the locale you want to pin. Find the last known good revision in the corresponding `l10n repo`_.

Create a commit that sets the ``pin`` boolean to ``true`` and the ``revision`` to the last known good revision, e.g.::

    "be": {
        "pin": false,
               ^^^^^
        "platforms": [
            "linux",
            "linux-devedition",
            "linux64",
            "linux64-devedition",
            "macosx64",
            "macosx64-devedition",
            "win32",
            "win32-devedition",
            "win64",
            "win64-aarch64",
            "win64-aarch64-devedition",
            "win64-devedition"
        ],
        "revision": "dffc49eb106ab53874de91b8a8f98ffc7c6bf9fc"
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    },

Make sure it's valid json afterwards, e.g.::

    python -mjson.tool l10n-changesets.json

Commit and `push the commit to phabricator <https://moz-conduit.readthedocs.io/en/latest/phabricator-user.html>`_ for review. Land on the target repo, by direct push, Autoland->Central merge, or sheriff uplift. We probably want to land it before the next set of nightlies or betas.

How to unpin an l10n revision
-----------------------------

This is likely the opposite of pinning.

One way is to back out the pinning commit. This is probably the least amount of work, but the bumper will need to run to update the revision.

The second way is to create a new commit: set ``pin`` to ``false``, and populate the ``revision`` with the latest `l10n repo`_ revision.

.. _l10n repo: https://hg.mozilla.org/l10n-central/
.. _l10n-changesets.json: https://hg.mozilla.org/mozilla-central/file/f788858ac268c25b4bc573d4a2642df44af22daa/browser/locales/l10n-changesets.json

.. _manually_trigger_l10n_bumper:

How to manually trigger l10n-bumper
-----------------------------------

Because we list l10n-bumper in the set of `manually triggerable cron tasks <https://hg.mozilla.org/ci/ci-configuration/file/2813f0e845f1561dc50daec9a9318035eefa42f8/projects.yml#l247>`_ in both central and beta, we have two manually triggerable hooks we can trigger at will.

- `Central hook <https://firefox-ci-tc.services.mozilla.com/hooks/project-releng/cron-task-mozilla-central%2Fl10n-bumper>`_
- `Beta hook <https://firefox-ci-tc.services.mozilla.com/hooks/project-releng/cron-task-releases-mozilla-beta%2Fl10n-bumper>`_

These will trigger a cron task which will schedule an l10n-bumper task. The l10n-bumper task should bump all unpinned locales' revisions to the latest, according to its in-tree configuration.
