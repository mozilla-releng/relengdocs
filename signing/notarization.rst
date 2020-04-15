Notarization
============

As of June 26, 2019, we started signing mac builds on the mac
notarization pool (Fx69). These tasks also notarize the signed builds,
and create signed pkg installers.

Machines
--------

A machine list is
`here <https://github.com/escapewindow/scriptworker-scripts/wiki/machines>`__.

We’re working on adding deployment support to
`ronin-puppet <https://github.com/mozilla-platform-ops/ronin_puppet/>`__.
Currently we need to ssh in to debug and deploy fixes.

General workflow
----------------

IScript will:

-  extract the files from a dmg
-  sign widevine and omnija (autograph signing)
-  sign mac, without the mac signing servers
-  create a zipfile of the .app files
-  send that zipfile to Apple for notarization
-  poll Apple for notarization status
-  on success, “staple” the notarization to the app
-  create tarballs of the .app files
-  create .pkg installers and sign them

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

Aki, Nick, and Simon know notarization the best, and can help debug.

Links
-----

-  https://github.com/escapewindow/scriptworker-scripts/wiki/Testing-iscript
-  https://github.com/escapewindow/scriptworker-scripts/wiki/manual-rollout
-  https://github.com/escapewindow/scriptworker-scripts/wiki/machines
-  https://trello.com/b/kyBE2ZIt/mac-notary
