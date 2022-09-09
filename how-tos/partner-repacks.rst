Partner Repacks
===============

Partner Repacks are where we take a built and signed Firefox desktop build and modify things (branding, plugins, prefs), potentially also do so for l10n repacks, then re-sign the new files. The main point of contact here will be Mike Kaply.

EME Free is a repacked Firefox without Encrypted Media Extensions, which allows you to run a Firefox without DRM (at the cost of broken video streaming).

How do I find the manifests and scripts?
----------------------------------------

These are configured in `taskcluster.ci.config.partner-urls <https://hg.mozilla.org/mozilla-central/file/c955747778a29618cf6347cd8722e1f60c7e100a/taskcluster/ci/config.yml#l423>`__.

For production, we use the largely-private `mozilla-partners org <https://github.com/orgs/mozilla-partners>`__. We have separate manifest repos for `release partners <https://github.com/mozilla-partners/repack-manifests>`__, `esr partners <https://github.com/mozilla-partners/esr-repack-manifests>`__, and `EME Free <https://github.com/mozilla-partners/mozilla-EME-free-manifest>`__.

For staging releases, we use the ``moz-releng-automation-stage`` bot's repositories: `staging release partners <https://github.com/moz-releng-automation-stage/repack-manifests>`__, `staging esr partners <https://github.com/moz-releng-automation-stage/esr-repack-manifests>`__, and `staging EME Free <https://github.com/moz-releng-automation-stage/mozilla-EME-free-manifest>`__.

The scripts are in `repack-scripts <https://github.com/mozilla-partners/repack-scripts>`__.

How do we add/remove partners?
------------------------------

This is via manifest manipulation. If we're adding a new partner, we'll need to create a partner repo first, before pointing to it in the manifest.

This has largely been out of Releng's hands, and we've only seen a reduction of the number of partners since the 2020 layoffs. These PRs have come from Kaply, e.g. `Remove unused partners #26 <https://github.com/mozilla-partners/repack-manifests/pull/26>`__.

How do I see partner tasks?
---------------------------

There are a ton of ``release-partner-repack-*`` and ``release-eme-free-*`` tasks in a given Firefox desktop RC or dot-release promote graph. Also `Firefox desktop betas >= b5 <https://github.com/mozilla-releng/shipit/blob/79bbd4c5b30234c54b238d064074399ea45a8803/api/src/shipit_api/admin/release.py#L99-L106>`__.

Many of these tasks might not be visible in Treeherder. We intentionally hid them, then decided to show them, but haven't finished that process. We probably want to make them visible for easier sheriffing of failed release tasks.

How do I find partner release artifacts?
----------------------------------------
EME-Free shows up in our candidates and releases directories on archive.m.o.

Some partner repacks are public, and we push those binaries to, e.g. https://archive.mozilla.org/pub/firefox/candidates/105.0b9-candidates/build1/partner-repacks/. Other partner repacks are private, and we push them to the partner bucket, which is not visible on archive.m.o.

We can also find the partner tasks and download their private artifacts.

Are there any known issues for partner repacks?
-----------------------------------------------

Beyond not being visible on Treeherder, we also don't grant scriptworker tasks the correct ``queue:get-artifact:releng/partner/*`` scopes (these are needed since partner artifacts are private). Instead, we grant these scopes to the worker ``clientId``'s. This blocks using the temporary credentials granted to the task, which is best practice. Once we grant the proper scopes, we can re-roll out the fix for `scriptworker #426 download artifacts with temp_queue if possible <https://github.com/mozilla-releng/scriptworker/issues/426>`__, and scriptworker will follow the same scopes pattern as docker- and generic-worker, where we use the scopes granted to the task rather than the scopes granted to the worker.
