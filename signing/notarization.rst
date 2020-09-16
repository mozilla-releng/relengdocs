Notarization
============

As of June 26, 2019, we started signing mac builds on the mac
notarization pool (Fx69). These tasks also notarize the signed builds,
and create signed pkg installers.

Machine and maintenance
-----------------------

The machine list is
`here <https://github.com/escapewindow/scriptworker-scripts/wiki/machines>`__.

We’re working on adding deployment support to
`ronin-puppet <https://github.com/mozilla-platform-ops/ronin_puppet/>`__.
We want to be able to fully automate rollout, from imaging to rollout. We also want to be able to bump dependency versions in ronin-puppet and have it Just Work. The todo list for those is `here <https://github.com/mozilla-releng/scriptworker-scripts/wiki/mac-todo>`__.

Until then, use these links:

- `testing iscript <https://github.com/mozilla-releng/scriptworker-scripts/wiki/Testing-iscript>`__
- `manual rollout with puppet <https://github.com/mozilla-releng/scriptworker-scripts/wiki/Manual-Rollout-with-Puppet>`__ for prod and tb-prod
- `manual rollout <https://github.com/mozilla-releng/scriptworker-scripts/wiki/manual-rollout>`__ for dep, until `bug 1648845 <https://bugzilla.mozilla.org/show_bug.cgi?id=1648845>`__ is fixed.

General workflow
----------------

In the ``mac_notarize`` behavior, iScript will:

-  extract the files from a dmg
-  sign widevine and omnija (autograph signing)
-  sign mac, without the mac signing servers
-  create .pkg installers and sign them
-  create a zipfile of the .app and .pkg files
-  send that zipfile to Apple for notarization
-  poll Apple for notarization status
-  on success, “staple” the notarization to the app
-  create tarballs of the .app files

However, we would often have issues in the polling step or otherwise end up wasting expensive signing worker cycles just sitting there idle.

To remedy this, we split notarization into three behaviors: ``mac_notarize_part_1``,
``notarization_poller``, and ``mac_notarize_part_3``.

In the ``mac_notarize_part_1`` behavior, iScript will:

- extract the files from a dmg
- sign widevine and omnija (autograph signing)
- sign mac, without the mac signign servers
- create a zipfile of the .app and .pkg files
- send that zipfile to Apple for notarization
- create tarballs of the .app files, unstapled
- upload the tarballs and .pkg files as artifacts, as well as a uuids json file.

In the ``notarization_poller`` task, ``notarization_poller`` will download the
uuids json file from the ``part_1`` task, and poll Apple. If they all return
complete, the task goes green. Otherwise the task will fail or throw an exception.

In the ``mac_notarize_part_3`` behavior, iScript will:

- download the tarballs and .pkg files from ``part_1``, staple the notarization,
  and upload

Debugging
---------

The code used is
`here <https://github.com/escapewindow/scriptworker-scripts/tree/master/iscript>`__.

An error like
``iscript.exceptions.TimeoutError: Timed out polling for uuid aa2dc2bc-9059-426e-a292-0bfb575a337b!``
means that Apple has taken too long to notarize. We may want to bump the
```notarization_poll_timeout`` <https://github.com/escapewindow/scriptworker-scripts/wiki/Testing-iscript#script_configyaml>`__
everywhere. Generally a rerun has fixed this issue.

Escalation
----------

Aki knows notarization the best, and can help debug.

Links
-----

-  https://github.com/escapewindow/scriptworker-scripts/wiki/Testing-iscript
-  https://github.com/escapewindow/scriptworker-scripts/wiki/manual-rollout
-  https://github.com/escapewindow/scriptworker-scripts/wiki/manual-rollout-with-puppet
-  https://github.com/escapewindow/scriptworker-scripts/wiki/machines
