Signing and Notarization
========================

Certificates
------------

For certificate rotation, see the signing page in `RelEng Confluence space <https://mozilla-hub.atlassian.net/wiki/spaces/RelEng/overview>`__.

Provisioning Profiles
---------------------

Since we started adding restricted entitlements to Firefox, Apple forces us to include a Provisioning Profile in the bundle.
Mozilla VPN also uses profiles.

For a summary of what a Provisioning Profile is, see `this article <https://itnext.io/apple-provisioning-profile-as-simple-as-possible-b2db0af94e5>`__.
At a minimum these are the things in each profile:

1. One App ID (aka Bundle ID). i.e.: ``org.mozilla.firefox``
2. One Certificate reference (this cert has to be provided by Apple)
3. The entitlements that are enabled for this "Identifier" (Bundle ID)
4. Devices (Only present in **Development** Provisioning Profiles!)

Given profiles have 1-to-1 relation to certificates, they need to be rotated at the same time.

At this point, profiles are stored in the workers under the ``provisionprofiles`` directory, and there is no automation around deploying them.

Notarization
------------

We currently notarize Firefox using `rcodesign <https://github.com/indygreg/apple-platform-rs/tree/main/apple-codesign>`__ (aka apple-codesign).
Using this rust tool allows us to notarize apps in Linux, more specifically in `signingscript <https://github.com/mozilla-releng/scriptworker-scripts/blob/master/signingscript/src/signingscript/rcodesign.py>`__.

Machines and maintenance
------------------------

The machine list is
`here <https://github.com/mozilla-releng/scriptworker-scripts/wiki/machines>`__.

We also keep quarantine and current status of each machine there.


Some deployment automation has been added to `ronin-puppet <https://github.com/mozilla-platform-ops/ronin_puppet/>`__.
We want to be able to fully automate rollout, from imaging to rollout. We also want to be able to bump dependency versions in ronin-puppet and have it Just Work.
The todo list for those is `here <https://github.com/mozilla-releng/scriptworker-scripts/wiki/mac-todo>`__.
As of November 2023, SRE is investigating an alternative method to image and maintain the Mac fleet. RelEng might use some of these tools to maintain the Mac signers.

Some useful wiki links:

- `testing iscript <https://github.com/mozilla-releng/scriptworker-scripts/wiki/Testing-iscript>`__
- `manual rollout with puppet <https://github.com/mozilla-releng/scriptworker-scripts/wiki/Manual-Rollout-with-Puppet>`__ for prod and tb-prod
- `manual rollout <https://github.com/mozilla-releng/scriptworker-scripts/wiki/manual-rollout>`__ for dep, until `bug 1648845 <https://bugzilla.mozilla.org/show_bug.cgi?id=1648845>`__ is fixed.
- `mac maintenance <https://github.com/mozilla-releng/scriptworker-scripts/wiki/mac-maintenance>`__ for how to update deps, restart scriptworker, and wipe machines.

General notarization workflow (DEPRECATED)
------------------------------------------

This behavior is deprecated, but still available, since ESR still uses it.
After ESR115 goes away, we should either delete this, or update to reflect the current workflow

In the ``mac_notarize`` behavior, iScript will:

- extract the files from a dmg
- sign widevine and omnija (autograph signing)
- sign mac, without the mac signing servers
- create .pkg installers and sign them
- create a zipfile of the .app and .pkg files
- send that zipfile to Apple for notarization
- poll Apple for notarization status
- on success, “staple” the notarization to the app
- create tarballs of the .app files

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
`here <https://github.com/mozilla-releng/scriptworker-scripts/tree/master/iscript>`__.

An error like
``iscript.exceptions.TimeoutError: Timed out polling for uuid aa2dc2bc-9059-426e-a292-0bfb575a337b!``
means that Apple has taken too long to notarize. We may want to bump the
```notarization_poll_timeout`` <https://github.com/mozilla-releng/scriptworker-scripts/wiki/Testing-iscript#script_configyaml>`__
everywhere. Generally a rerun has fixed this issue.

Escalation
----------

@hneiva knows notarization the best, and can help debug.

Links
-----

- https://github.com/mozilla-releng/scriptworker-scripts/wiki/Testing-iscript
- https://github.com/mozilla-releng/scriptworker-scripts/wiki/manual-rollout
- https://github.com/mozilla-releng/scriptworker-scripts/wiki/manual-rollout-with-puppet
- https://github.com/mozilla-releng/scriptworker-scripts/wiki/machines
- https://github.com/mozilla-releng/scriptworker-scripts/wiki/machines
- https://github.com/mozilla-releng/scriptworker-scripts/tree/master/signingscript
- https://github.com/indygreg/apple-platform-rs/tree/main/apple-codesign
- https://github.com/mozilla-platform-ops/ronin_puppet
