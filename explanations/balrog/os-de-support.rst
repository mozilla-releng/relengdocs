Ending Firefox Support for an Operating System
==============================================

From time to time, Firefox drops support for an OS: for example, Firefox was once available on Windows XP, but it isn't today. Typically, de-support for an OS is timed to coincide with an ESR release and Firefox users on the de-supported OS are migrated to the ESR channel.

There are several Release Engineering activities required to ensure support is ended cleanly.

(This section is based on the experience of de-supporting macOS 10.12/.13/.14, `bug 1836375 <https://bugzilla.mozilla.org/show_bug.cgi?id=1836375>`__.)

Preparation
~~~~~~~~~~~

* If there is no meta-bug for the de-support work, `create one <https://bugzilla.mozilla.org/show_bug.cgi?id=1836375>`__.
* There should be a bug for publishing a SUMO KB article announcing the end of support. Ensure the SUMO KB bug blocks the meta-bug.
* Note the Firefox version when support is ending. For example, the `KB article announcing end of support for macOS 10.12 <https://support.mozilla.org/kb/firefox-users-macos-1012-1013-1014-moving-to-extended-support>`__ says "Firefox version 115 will be the last supported Firefox version for users of macOS 10.12".
* In addition to the Balrog changes described here, changes to Bedrock and Bouncer will probably be needed; try to coordinate these as early as possible.
* Until the SUMO KB article has been published, ensure any related bugs are **Confidential**.

Create a new channel-switching mar
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Get a copy of the `'mar' executable <https://archive.mozilla.org/pub/firefox/candidates/114.0b9-candidates/build1/mar-tools>`__
* Get a copy of `create-channel-switch-mar.py <https://hg.mozilla.org/build/braindump/file/tip/update-related/create-channel-switch-mar.py>`__
* Create a new mar with the script, something like:::

    create-channel-switch-mar.py --version 115.0 --channel esr --accepted-channel-id firefox-mozilla-esr --mar-channel-id firefox-mozilla-release --distribution-id mozilla-mac-eol-esr115 --output switch-to-esr115.0-eol-mac.mar

* Examine your mar. Note that mar contents are xz (or bzip2) compressed, even after extraction.::

    mar -T switch-to-esr115.0-eol-mac.mar
    mar -x switch-to-esr115.0-eol-mac.mar
    xz -c -d updatev3.manifest

* Verify your mar. :doc:`/how-to/test/updates` describes how to apply a mar manually.
* Sign the mar via adhoc_signing. See https://github.com/mozilla-releng/adhoc-signing/blob/main/signing-manifests/bug1835022.yml for a sample manifest. 

Copy the channel-switching mar to archive.mozilla.org
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Channel-switching mar files are typically copied to https://archive.mozilla.org/pub/firefox/releases/custom-updates/. You may want to file a bug like `bug 1839195 <https://bugzilla.mozilla.org/show_bug.cgi?id=1839195>`__.

Balrog updates
~~~~~~~~~~~~~~

Each Firefox channel likely needs a new rule in Balrog.

Broadly there are 3 behaviors of interest:

* ESR-SWITCH: switch de-supported users to the ESR channel using a channel-switching mar
* DE-SUPPORT: allow updates to the most recent supported version on the channel, then serve a "de-support" update which points to the relevant KB article
* NO-UPDATE: stop all updates temporarily

Typically NO-UPDATE is used to stop updates temporarily just before the first unsupported version is available on each channel. Once the last supported version is available, an ESR-SWITCH or DE-SUPPORT rule is implemented and the NO-UPDATE rule is deleted.

Update Balrog rules for Nightly
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For the Nightly channel, we usually DE-SUPPORT.

Just *before* the first nightly build (could be a few days earlier, if convenient) of the first unsupported version, pause Nightly updates for the affected OS version: 

* Create a new rule matching the ``Firefox : nightly*`` channel and the OS version to serve the ``No-Update`` release.

Shortly *after* the first nightly build of the first unsupported version:

* Determine the build ID of the last build of the last supported version: You might check `archive.mozilla.org <https://archive.mozilla.org/pub/firefox/nightly/>`__ for instance.
* Update the ``Firefox-mozilla-central-nightly-<buildid>`` Release blob, to include aliases (this is only required on the Nightly channel, as it is caused by `bug 1810740 <https://bugzilla.mozilla.org/show_bug.cgi?id=1810740>`__). Copy the list of aliases from the ``Firefox-mozilla-central-nightly-latest`` release; it should look something like::

    "Darwin_aarch64-gcc3": {
      "alias": "Darwin_x86_64-gcc3-u-i386-x86_64"
    },
    "Darwin_x86-gcc3": {
      "alias": "Darwin_x86_64-gcc3-u-i386-x86_64"
    },
    "Darwin_x86-gcc3-u-i386-x86_64": {
      "alias": "Darwin_x86_64-gcc3-u-i386-x86_64"
    },
    "Darwin_x86_64-gcc3": {
      "alias": "Darwin_x86_64-gcc3-u-i386-x86_64"
    },
    "WINNT_x86-msvc-x64": {
      "alias": "WINNT_x86-msvc"
    },
    "WINNT_x86-msvc-x86": {
      "alias": "WINNT_x86-msvc"
    },    
    "WINNT_x86_64-msvc-x64": {
      "alias": "WINNT_x86_64-msvc"
    },    

* Create a rule to pin `nightly*` users to the most recent supported version: match the ``Firefox : nightly*`` channel, the affected OS version and build ID < latest supported build ID determined above; serve the Release corresponding to that build ID, modified earlier, ``Firefox-mozilla-central-nightly-<buildid>``.
* Create a new ``De-Support`` Release referencing the SUMO KB article. Careful: Use a locale-agnostic link like https://support.mozilla.org/kb/firefox-users-macos-1012-1013-1014-moving-to-extended-support (instead of https://support.mozilla.org/en-US/kb/firefox-users-macos-1012-1013-1014-moving-to-extended-support). Example release blob: ::

    {
        "detailsUrl": "https://support.mozilla.org/kb/firefox-users-macos-1012-1013-1014-moving-to-extended-support",
        "displayVersion": "115.0",
        "name": "OSX-10.12-10.14-Desupport",
        "product": "Firefox",
        "schema_version": 50
    }

* Create a rule to serve the de-support notice: match the ``Firefox : nightly*`` channel and the affected OS version with lower priority than the pinning rule (so probably those who have been updated to the last supported build); serve the new ``De-Support`` release created earlier.
* Delete the ``No-Update`` rule created earlier.

Update Balrog rules for Aurora
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Check with the *Product* organization to verify per-channel requirements for DevEdition.

To implement DE-SUPPORT for DevEdition, follow the de-support procedure for Nightly, above, with these changes:

* Make changes just before and after the Merge Day II merge of central to beta.
* Use the ``Firefox : aurora*`` channel
* There should be no need to add aliases to the release blob.

Update Balrog rules for Beta and Release
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Check with the *Product* organization to verify per-channel requirements for Beta and Release.

For these channels, we generally ESR-SWITCH: serve an update referencing the channel-switching MAR, so that users on the affected OS move from the Beta or Release channel to the ESR channel.

First, create the channel-switching release, which will serve the channel-switching mar created earlier. To create the release blob:

* Get the `create_channel_switch_blob.py script <https://hg.mozilla.org/build/braindump/file/tip/releases-related/create_channel_switch_blob.py>`__
* Use the script to create a local json file containing the blob; something like: ::

    create_channel_switch_blob.py https://archive.mozilla.org/pub/firefox/releases/custom-updates/switch-to-esr115.0-eol-win.mar https://aus5.mozilla.org/api/v1/releases/Firefox-115.0b9-build1 WIN 115.0 20230630161221 win-channel-switch.json

* Check the json file; it may require some hand editing.
* In Balrog, create a new release using the generated json file.

Shortly after Merge Day I (during RC week), create ``localtest`` rules so that QA can verify end-to-end behavior:

* Create a new rule matching the ``Firefox : beta-localtest`` channel and the OS version to serve the channel-switching release. Do the same for ``Firefox : release-localtest``.
* Coordinate with *QA* to verify that the channel-switch works on Firefox (when configured for ``beta-localtest``).

Just before Merge Day II (central to beta merge), pause updates for affected OSes, on Beta.

* Create a new rule matching the ``Firefox : beta`` channel and the OS version to serve the ``No-Update`` release, or to pin to the last supported beta.

On Merge Day II:

* Duplicate the ``beta-localtest`` rule for the ``Firefox : beta-cdntest`` and ``Firefox : release-cdntest`` channels.
* Coordinate with *QA* if additional ``cdntest`` testing is desired.
* Expand the ``beta-localtest`` rule to ``Firefox : beta*``.
* If needed, delete the ``No-Update`` rule created earlier.

Coordinate with *Product* to determine the timing for changes to the ``release`` channel. We might want to expand the channel-switch for ``Firefox : release*`` at the same time as ``beta``, or we may wait until the end of the next release cycle.

Update Balrog rules for ESR
~~~~~~~~~~~~~~~~~~~~~~~~~~~

When the ESR branch providing the last support for a de-supported OS goes EOL, we typically pin the ``Firefox : esr*`` channel to the latest supported release and de-support.

Verify changes: Balrog responses
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Currently Firefox queries the Balrog production server with something like::

    https://aus5.mozilla.org/update/6/%PRODUCT%/%VERSION%/%BUILD_ID%/%BUILD_TARGET%/%LOCALE%/%CHANNEL%/%OS_VERSION%/%SYSTEM_CAPABILITIES%/%DISTRIBUTION%/%DISTRIBUTION_VERSION%/update.xml
    
For example, to verify the Nightly de-support rule, use the affected VERSION and OS_VERSION and the BUILD_ID of the pinned version: ::

    https://aus5.mozilla.org/update/6/Firefox/115.0a1/20230605094751/Darwin_x86_64-gcc3/en-US/nightly/Darwin%2017/default/default/default/update.xml
    
and check that the response serves the url of the SUMO KB article.::

    <?xml version="1.0"?>
    <updates>
        <update type="minor" unsupported="true" detailsURL="https://support.mozilla.org/kb/firefox-users-macos-1012-1013-1014-moving-to-extended-support" displayVersion="115.0">
        </update>
    </updates> 


To verify the Nightly pinning rule, change the BUILD_ID to an earlier build: ::

    https://aus5.mozilla.org/update/6/Firefox/115.0a1/20230505094751/Darwin_x86_64-gcc3/en-US/nightly/Darwin%2017/default/default/default/update.xml
    
and check that the response updates to the pinned build (eg. 20230605094751): ::

    <?xml version="1.0"?>
    <updates>
        <update type="minor" displayVersion="115.0a1" appVersion="115.0a1" platformVersion="115.0a1" buildID="20230605094751">
            <patch type="complete" URL="https://archive.mozilla.org/pub/firefox/nightly/2023/06/2023-06-05-09-47-51-mozilla-central/firefox-115.0a1.en-US.mac.complete.mar" hashFunction="sha512" hashValue="b9923d0267a946a44e18ef61a9c015fc9a6d75618a3dd49e6fcd596a4b1f5350cf0670e46f300adc88a5bbcd4019028970aabc36b8b986eb0e69941a163e85af" size="113713230"/>
        </update>
    </updates>

Verify changes: Application behavior
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* :doc:`/how-to/test/updates` describes how to apply a mar manually.
* QA usually verifies Firefox update behavior on each affected platform using trial rules on the ``beta-localtest`` channel prior to Merge Day II.

Stop running tests
~~~~~~~~~~~~~~~~~~

Does CI run tests on the deprecated OS? Coordinate with the CI Automation team to ensure taskcluster configs are updated to stop running tests on the de-supported test platform.

Update docs
~~~~~~~~~~~

File a `bug <https://bugzilla.mozilla.org/show_bug.cgi?id=1837652>`__ blocking the meta-bug to update the `docs <https://hg.mozilla.org/mozilla-central/file/default/docs/update-infrastructure/index.md>`__. Once the ESR-SWITCH is implemented for the Release channel, add a bullet to the list of "desupports".

