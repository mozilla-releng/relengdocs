OpenH264 updates
================

OpenH264 is a codec plugin allowing Firefox users to use WebRTC.
We provide updates via Balrog.

When
----

The request comes from the media team. The latest bug is
`this one. <https://bugzilla.mozilla.org/show_bug.cgi?id=1774221>`__

The last two updates happened because of changes on the Mac side (the M1
chip requiring eac arm support, macOS Monterey making notarization requirements
more strict).

How
---

Builds
~~~~~~

The `openh264-plugin kind <https://searchfox.org/mozilla-central/source/taskcluster/ci/openh264-plugin/kind.yml>`__ automates builds. We can update the `revision <https://searchfox.org/mozilla-central/rev/49566d906ad040cf233b0a5acd597e1a63b92f72/taskcluster/ci/openh264-plugin/kind.yml#23>`__ we pull from the Cisco repo (to date we seem to pull from `firefox-specific branches <https://github.com/cisco/openh264/branches/all?query=firefox>`__).

Ideally these builds Just Work, but since we don't currently run these regularly, most likely there will be `bustage <https://bugzilla.mozilla.org/show_bug.cgi?id=1774669#c1>`__.

Signing
~~~~~~~

We also have an `openh264-signing kind <https://searchfox.org/mozilla-central/source/taskcluster/ci/openh264-signing/kind.yml>`__; if we add-new-jobs these tasks, we should get signed builds.

However, we need to mac sign-and-notarize the mac binaries; as of 2022.06.16 we only gpg-detached-sign these. `bug 1774669 <https://bugzilla.mozilla.org/show_bug.cgi?id=1774669>`__ to automate this; currently we only have the `manual steps documented <https://docs.google.com/document/d/1HlfqJR-UhPNj9uxKs8RvW9_HIZkt2SgepLNErnk-6g8/edit?pli=1#heading=h.kcvjjvjdeu95>`__

Uploading to Cisco
~~~~~~~~~~~~~~~~~~

Currently we only `allowlist ciscobinary.openh264.org <https://github.com/mozilla-releng/balrog/blob/940d5865531b75e4d5cca49cde794b9f533234c9/uwsgi/public.wsgi#L25>`__ as a valid domain to download binaries for balrog.

That step is manual: send an `email or bugzilla needinfo <https://docs.google.com/document/d/1HlfqJR-UhPNj9uxKs8RvW9_HIZkt2SgepLNErnk-6g8/edit?pli=1#heading=h.jib81vs55t6t>`__.

Create the Balrog release
~~~~~~~~~~~~~~~~~~~~~~~~~

Create a new release and upload the new blob to Balrog:
    - on https://balrog.services.mozilla.com/releases click the “Add new release” button;
    - on the Create Release page, select "OpenH264" as the Product;
    - on the Create Release page, click "Upload Release" and select the file containing the new release blob;
    - verify that the new release blob has been uploaded and the "Release" name correctly identifies the release (eg. "OpenH264-1.8.1.2");
    - on the Create Release page, click "Create Release" button in the lower right to create the release.

(It may be easier to download the previous-good blob to edit than to create the blob from scratch; it will look similar to `OpenH264-1.8.1.2 <https://github.com/mozilla-releng/systemaddons-wip/blob/4c70d973a71ddf6cabf7dffd1ed95a0eb7bec912/existing/OpenH264/releases/OpenH264-1.8.1.2.yml>`__, except in json format.)

Create the Balrog rule
~~~~~~~~~~~~~~~~~~~~~~

Create a new rule to test the release on the nightlytest channel:
    - on https://balrog.services.mozilla.com/rules click the “Add Rule" button
    - on the Create Rule page, set Product = "OpenH264", Channel = "nightlytest" (or as needed), Mapping = the release you just created, Background Rate = 100 (or as needed), and set the Priority as needed, typically the lowest priority for the default rule.
    - on the Create Rule page, click "Create Rule" button in the lower right to create the rule.

See https://mozilla-balrog.readthedocs.io/en/latest/database.html for
general guidance on rule matching.

OpenH264 updates are generally sent to all channels, though we can restrict by update channel (e.g. ``esr*`` to only target esr users or nightlytest, the internal testing channel). This means users are given a new OpenH264 plugin based on their Firefox version. For instance: if we provide a new OpenH264 to 98.0 at the time 98.0b15 ships, then users with 98.0b1-b14 will also get this version. Make sure with the media team these betas are compatible! In the case it's not, please remember Firefox doesn't send which beta it's on to Balrog. You have to filter out based on the version **and** the buildID (the buildID alone doesn't work if a 97 dot release happens afterwards).

Testing
~~~~~~~

You can use the nightlytest channel to test changes before sending them
to production. An OpenH264 request to balrog is like this one:
https://aus5.mozilla.org/update/3/GMP/102.0/20180802174131/WINNT_x86_64-msvc-x64/en-US/nightlytest/default/default/default/update.xml
