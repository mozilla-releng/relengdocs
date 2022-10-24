Android L10n
============

Also see `Continuous Localization Setup Process for Android <https://mana.mozilla.org/wiki/pages/viewpage.action?spaceKey=FIREFOX&title=Continuous+Localization+Setup+Process+for+Android>`__.

Similar to desktop's :ref:`l10n_cross_channel`, `android-l10n-tooling <https://github.com/mozilla-l10n/android-l10n-tooling/>`__ takes en-US strings from mobile repos and lands them in quarantine branches in the `android-l10n repo <https://github.com/mozilla-l10n/android-l10n>`__. (These are likely named ``-quarantine`` for similar reasons to the naming in :ref:`l10n_cross_channel`: there, a human looks at the quarantined changes and decides whether to uplift.) This is an `example PR <https://github.com/mozilla-l10n/android-l10n/pull/483>`__ created by android-l10n-tooling.

It also takes localized strings and opens pull requests from the mobile repos (Fenix, Android-Components, and Focus-Android).

How to find the most recent update-l10n tasks
---------------------------------------------
Go to the `update-l10n hook`_. The recent history of update-l10n hook triggers should be listed here. Note that most or all of these are triggered by a ``PULSE MESSAGE``; see :ref:`pulse_triggered_cron_hooks`.

To view one of these, click on one of the ``taskId``'s. Note the ``HOOK_PAYLOAD`` in the ``task.payload.env``, which is a handy way of transmitting information, unless the `file list exceeds the max size for this field <https://github.com/mozilla-l10n/android-l10n-tooling/issues/28>`__.

In the log file you'll see a line like::

    Task Id: CCR2IZxhTDygMHptMuAUzQ

This is the ``taskId`` of the decision task that runs ``update-l10n`` against the supported repositories.

How to trigger the update-l10n hook manually
--------------------------------------------

Go to the `update-l10n hook`_ and hit ``trigger hook``.

How to debug the update-l10n hook
---------------------------------

This is a tricky one. We've had trouble getting this working again when we made changes (renaming branches, adding new repos, etc.) We likely want to flesh out this documentation the next time we hit issues.

How to find the most recent update-projects tasks
-------------------------------------------------

Go to the `android-l10n-tooling hook`_ and find the task that triggered at 0:00 UTC (or whenever is listed in `.cron.yml <https://github.com/mozilla-l10n/android-l10n-tooling/blob/master/.cron.yml>`__ for ``update-projects``).

In the log file you'll see a line like::

    Task Id: Nf3ItL-jQ5qBzJ3zklC46Q

This is the ``taskId`` of the decision task that runs ``update-projects`` against the supported repositories.

How to trigger the update-projects hook manually
------------------------------------------------

Go to the  `update-projects hook`_ and hit ``trigger hook``.

How do I find known android-l10n-tooling issues?
------------------------------------------------

We've filed issues under the `android-l10n-tooling repo <https://github.com/mozilla-l10n/android-l10n-tooling/issues>`__.

.. _update-l10n hook: https://firefox-ci-tc.services.mozilla.com/hooks/project-releng/cron-task-mozilla-l10n-android-l10n-tooling%2Fupdate-l10n

.. _android-l10n-tooling hook: https://firefox-ci-tc.services.mozilla.com/hooks/project-releng/cron-task-mozilla-l10n-android-l10n-tooling
.. _update-projects hook: https://firefox-ci-tc.services.mozilla.com/hooks/project-releng/cron-task-mozilla-l10n-android-l10n-tooling%2Fupdate-projects
