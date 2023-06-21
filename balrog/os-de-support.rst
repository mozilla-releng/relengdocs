Ending Firefox Support for an Operating System
==============================================

From time to time, Firefox drops support for an OS: for example, Firefox was once available on Windows XP, but it isn't today. Typically, de-support for an OS is timed to coincide with an ESR release and Firefox users on the de-supported OS
are migrated to the ESR channel.

There are several Release Engineering activities required to ensure support is ended cleanly.

(This section is based on the experience of de-supporting macOS 10.12/.13/.14, `bug 1836375 <https://bugzilla.mozilla.org/show_bug.cgi?id=1836375>`__.)

Preparation
~~~~~~~~~~~

* If there is no meta-bug for the de-support work, `create one <https://bugzilla.mozilla.org/show_bug.cgi?id=1836375>`__.
* There should be a bug for publishing a SUMO KB article announcing the end of support. Ensure the SUMO KB bug blocks the meta-bug.
* Note the Firefox version when support is ending. For example, the `KB article announcing end of support for macOS 10.12 <https://support.mozilla.org/kb/firefox-users-macos-1012-1013-1014-moving-to-extended-support>`__ says "Firefox version 115 will be the last supported Firefox version for users of macOS 10.12".
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

* Sign the mar via adhoc_signing. See https://github.com/mozilla-releng/adhoc-signing/blob/main/signing-manifests/bug1835022.yml for a sample manifest. 
* Upload the new signed mar to https://archive.mozilla.org/pub/firefox/releases/custom-updates/ via a bug like bug 

Verify the channel-switching mar
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TBD

Copy the channel-switching mar to archive.mozilla.org
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Channel-switching mar files are typically copied to https://archive.mozilla.org/pub/firefox/releases/custom-updates/.
You may want to file a bug like `bug 1839195 <https://bugzilla.mozilla.org/show_bug.cgi?id=1839195>`__.

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

Just *before* the first nightly build (could be a few days earlier, if convenient) of the first unsupported version,
pause Nightly updates for the affected OS version: 

* Create a new rule matching the Firefox : Nightly* channel and the OS version to serve the NoUpdate release.

Shortly *after* the first nightly build of the first unsupported version:

* Determine the build ID of the last build of the last supported version: You might check `archive.mozilla.org <https://archive.mozilla.org/pub/firefox/nightly/>`__ for instance.
* Create a rule to pin Nightly* users to the most recent supported version: match the Firefox : Nightly* channel, the affected OS version and build ID < latest supported build ID determined above; serve the Release corresponding to that build ID.
* Update the Release referenced by the new pinning rule, to include aliases (this is only required on Nightly, as it is caused by `bug 1810740 <https://bugzilla.mozilla.org/show_bug.cgi?id=1810740>`__): Update the Release blob by adding aliases like::

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
    "WINNT_x86_64-msvc-x64": {
      "alias": "WINNT_x86_64-msvc"
    },    

* Create a new De-Support release referencing the SUMO KB article. Careful: Use a locale-agnostic link like https://support.mozilla.org/kb/firefox-users-macos-1012-1013-1014-moving-to-extended-support (instead of https://support.mozilla.org/en-US/kb/firefox-users-macos-1012-1013-1014-moving-to-extended-support). Example release blob: ::

    {
        "detailsUrl": "https://support.mozilla.org/kb/firefox-users-macos-1012-1013-1014-moving-to-extended-support",
        "displayVersion": "115.0",
        "name": "OSX-10.12-10.14-Desupport",
        "product": "Firefox",
        "schema_version": 50
    }

* Create a rule to serve the de-support notice: match the Firefox : Nightly* channel and the affected OS version with lower priority than the pinning rule (so probably those who have been updated to the last supported build); serve the new De-Support release.
* Delete the NoUpdate rule created earlier.

Update Balrog rules for Beta and Aurora
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Check with the *Product* organization to verify per-channel requirements for Beta and DevEdition.

To implement DE-SUPPORT for DevEdition, follow the de-support procedure for Nightly, above, with these changes:

* Make changes just before and after the Merge Day II merge of central to beta.
* Use the Firefox : aurora* channel
* There should be no need to add aliases to the release blob.

To implement ESR-SWITCH for Beta, follow the de-support procedure for Release, below, with these changes:

* Make changes just before and after the Merge Day II merge of central to beta.
* Use the Firefox : beta* channel

Update Balrog rules for Release
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For the Release channel, we generally ESR-SWITCH: serve an update referencing the channel-switching MAR, so that
users on the affected OS move from the Release channel to the ESR channel.

Just *before* the first release build of the first unsupported version, pause Release updates for the affected OS version. This will typically be just before the Merge Day I merge of Beta to Release, for the release after the Beta changes.

* Create a new rule matching the Firefox : Release* channel and the OS version to serve the NoUpdate release.

Shortly *after* the first release build of the first unsupported version:

* Create a new release to serve the channel-switching mar. *TBD: do we duplicate an existing release, then manually replace the url?*
* Create a new rule matching the Firefox : Release* channel and the OS version to serve the channel-switching release.
* *TBD: Is that all, or do we need pinning?*
* Delete the NoUpdate rule created earlier.
 
Update Balrog rules for ESR
~~~~~~~~~~~~~~~~~~~~~~~~~~~

TBD

* Like https://bugzilla.mozilla.org/show_bug.cgi?id=1275609 ?
* Pin and de-support?
* How do we remember to do this? File a bug now and .... ?

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

TBD

Stop running tests
~~~~~~~~~~~~~~~~~~

Does CI run tests on the deprecated OS? Coordinate with the CI Automation team to ensure taskcluster configs are updated to stop running tests on the de-supported test platform.

Update docs
~~~~~~~~~~~

File a `bug <https://bugzilla.mozilla.org/show_bug.cgi?id=1837652>`__ blocking the meta-bug to update the `docs <https://hg.mozilla.org/mozilla-central/file/tip/docs/update-infrastructure/index.md>`__. Once the ESR-SWITCH is implemented for the Release channel, add a bullet to the list of "desupports".

