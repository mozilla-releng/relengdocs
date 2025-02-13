################################
Debugging Update Verify Failures
################################

Before doing this, you should familiarize yourself with `how update verify works <https://firefox-source-docs.mozilla.org/tools/update-verify/index.html>`__.


*****
When?
*****

When update verify tasks fail it is your responsibility as releaseduty to analyze them and determine whether or not any action needs to be taken for any differences found.

You may also be responsible for looking over update verify logs if changes have been made or there are other reasons to believe that we need some manual verification of update verify logs even when things are green. (For example, if there were update verify issues in a previous release, we commonly want extra verification of the next release's update verify logs.)

****
How?
****

Download the logs locally
=========================
There are a heck of a lot of update verify logs in your typical release graph. It's often useful to download them and look at them locally instead of using the Taskcluster UI or raw log in the browser. This should help you do that. Be careful only to run it after all jobs have completed (running jobs won't have their logs available, and you don't want half finished logs anyways):

.. code-block:: bash

    task_group_id=xxxxxxx
    mkdir -p update-verify-logs
    taskcluster group list -a $task_group_id --format-string "{{ .Status.TaskID }} {{ .Task.Metadata.Name }}" | grep ".* release-update-verify" | cut -d' ' -f1 | xargs -I {} sh -c "echo 'Getting log for {}'; taskcluster task log {} > update-verify-logs/{}.log"

Analyzing the full log
======================

Update verify logs are quite verbose and can be intimidating to look at! But don't fear, although there's a lot of output, very little of it is typically relevant.

Log structure
-------------

Set-up and preamble
^^^^^^^^^^^^^^^^^^^

Each log begins with a bit of set-up, most notably the downloading the update verify configuration file. In the vast majority of cases, this is irrelevant. Once we get to the following block:

::

    command: START
    command: bash verify.sh -c /tmp/tmp93urvqms
    command: cwd: /builds/worker/checkouts/gecko/tools/update-verify/scripts/../release/updates
    command: env: {'DIFF_SUMMARY_LOG': '/builds/worker/checkouts/gecko/diff-summary.log'}
    command: output:
    Using config file /tmp/tmp93urvqms

...the actual testing begins.

After this each individual test begins with a log message beginning with ``Using  https://....``, for example:

::

    Using  https://aus5.mozilla.org/update/3/Firefox/136.0/20250207091649/Linux_x86-gcc3/br/aurora-localtest/default/default/default/update.xml?force=1

...note the two spaces after "Using", which makes it easy to find the start of a new test block (and by extension, the end of the previous test).

Each individual test is either a ``COMPLETE`` test or a ``TEST_ONLY`` test. Expected output differs between these two types.


Complete tests
^^^^^^^^^^^^^^

At the start of each test block we fetch 4 or 5 things:

* An update.xml from Balrog
* A MAR file that the response from Balrog points at
* The full installer for the ``from`` release
* The full installer for the ``to`` release
* The linux64 updater package (except on 32-bit and 64-bit Linux)

Any fetches of new files are logged verbosely, which can be quite noisy. (This output is helpful in cases where we, eg: see issues with remote servers or caches, but not in analyzing "true" update verify failures.)

Also as part of this we consider whether or not we need to replace certificates in the updater binary, resulting in output like this. This only happens for staging releases, where we are sometimes mixing dep and non-dep signing:

.. code-block:: text

    Found updater at updater
    Replacing certs in updater binary
    Looking for nightly_aurora_level3_primary.der...
    Didn't find nightly_aurora_level3_primary.der...
    Looking for nightly_aurora_level3_secondary.der...
    Didn't find nightly_aurora_level3_secondary.der...
    Looking for release_primary.der...
    Replacing release_primary.der with dep1.der
    Looking for release_secondary.der...
    Replacing release_secondary.der with dep2.der
    Looking for sha1/release_primary.der...
    Didn't find sha1/release_primary.der...
    Looking for sha1/release_secondary.der...
    Didn't find sha1/release_secondary.der...

We then decide how we need to invoke the updater:

.. code-block:: text

    + /builds/worker/checkouts/gecko/tools/update-verify/release/updates/updater/firefox/updater --help
    + grep which-invocation
    Usage: updater arg-version patch-dir install-dir apply-to-dir which-invocation [wait-pid [callback-working-dir callback-path args...]]
    + echo 'Using v3 arguments to updater...'
    Using v3 arguments to updater...

Finally, we start the test by invoking the updater. The beginning of this looks as follows:

.. code-block:: text

    + echo 'Calling updater:' /builds/worker/checkouts/gecko/tools/update-verify/release/updates/updater/firefox/updater 3 /builds/worker/checkouts/gecko/tools/update-verify/release/updates/update /builds/worker/checkouts/gecko/tools/update-verify/release/updates/source/firefox /builds/worker/checkouts/gecko/tools/update-verify/release/updates/source/firefox first 0
    Calling updater: /builds/worker/checkouts/gecko/tools/update-verify/release/updates/updater/firefox/updater 3 /builds/worker/checkouts/gecko/tools/update-verify/release/updates/update /builds/worker/checkouts/gecko/tools/update-verify/release/updates/source/firefox /builds/worker/checkouts/gecko/tools/update-verify/release/updates/source/firefox first 0
    + /builds/worker/checkouts/gecko/tools/update-verify/release/updates/updater/firefox/updater 3 /builds/worker/checkouts/gecko/tools/update-verify/release/updates/update /builds/worker/checkouts/gecko/tools/update-verify/release/updates/source/firefox /builds/worker/checkouts/gecko/tools/update-verify/release/updates/source/firefox first 0
    Unable to init server: Could not connect: Connection refused
    + set +x
    2025-02-08 00:46:49+0000: sUsingService=false
    2025-02-08 00:46:49+0000: sUpdateSilently=false
    2025-02-08 00:46:49+0000: isElevated=false
    2025-02-08 00:46:49+0000: gInvocation=UpdaterInvocation::First
    2025-02-08 00:46:49+0000: Writing status to file: applying
    2025-02-08 00:46:49+0000: PATCH DIRECTORY /builds/worker/checkouts/gecko/tools/update-verify/release/updates/update
    2025-02-08 00:46:49+0000: INSTALLATION DIRECTORY /builds/worker/checkouts/gecko/tools/update-verify/release/updates/source/firefox
    2025-02-08 00:46:49+0000: WORKING DIRECTORY /builds/worker/checkouts/gecko/tools/update-verify/release/updates/source/firefox
    2025-02-08 00:46:49+0000: UPDATE TYPE complete
    2025-02-08 00:46:49+0000: PREPARE REMOVEFILE vaapitest

Note the unfortunate ``Connection refused`` message here. This is the updater telling us that it can't show any UI, because we run these tests headless. This is a non-fatal error, but we log all output from the updater, so it will be present.

The output from the updater continue for a hundred or so lines starting with ``PREPARE``, ``EXECUTE``, or ``FINISH``. When those are done, the last few lines of output from the updater are expected to be:

.. code-block:: text

    2025-02-08 00:46:54+0000: succeeded
    2025-02-08 00:46:54+0000: Writing status to file: succeeded
    
    2025-02-08 00:46:54+0000: calling QuitProgressUI
    2025-02-08 00:46:54+0000: Running LaunchCallbackAndPostProcessApps
    2025-02-08 00:46:54+0000: No callback arg. Skipping LaunchWinPostProcess and LaunchCallbackApp

After this, we compare the applied update to the full installer of the ``to`` build. This output varies, but at minimum we expect to see the following for a passing test:

.. code-block:: text

    Comparing source/firefox with target/firefox...
    ignoring paths: ['Contents/CodeResources', 'Contents/embedded.provisionprofile']
    No differences found

If any unexpected differences are found, they will cause the test to fail and an entry to be added to ``diff-summary.log``.

After this, a new test will start, beginning with a ``Using  https://`` line.

Test-only tests
^^^^^^^^^^^^^^^

These tests are a subset of the complete tests. Specifically, they download:

* An update.xml from Balrog
* A MAR file that the response from Balrog points at

...and that's it. The test is considered a pass if Balrog points at a MAR, and that MAR can be downloaded or retrieved from the cache. The expected log output is debugging output from these operations, such as:

.. code-block:: text

    Downloading 'https://stage.balrog.nonprod.cloudops.mozgcp.net/update/3/Firefox/140.0/20250107203817/Linux_x86_64-gcc3/en-CA/beta-localtest/default/default/default/update.xml?force=1' and placing in cache...
    --2025-02-08 00:47:17--  https://stage.balrog.nonprod.cloudops.mozgcp.net/update/3/Firefox/140.0/20250107203817/Linux_x86_64-gcc3/en-CA/beta-localtest/default/default/default/update.xml?force=1
    Resolving stage.balrog.nonprod.cloudops.mozgcp.net (stage.balrog.nonprod.cloudops.mozgcp.net)... 35.244.151.186, 2600:1901:0:e99a::
    Connecting to stage.balrog.nonprod.cloudops.mozgcp.net (stage.balrog.nonprod.cloudops.mozgcp.net)|35.244.151.186|:443... connected.
    HTTP request sent, awaiting response... 
      HTTP/1.1 200 OK
      Server: nginx
      Date: Sat, 08 Feb 2025 00:47:17 GMT
      Content-Type: text/xml; charset=utf-8
      Content-Length: 769
      Vary: Accept-Encoding
      Rule-ID: 25
      Rule-Data-Version: 1231
      Strict-Transport-Security: max-age=31536000;
      X-Content-Type-Options: nosniff
      Content-Security-Policy: default-src 'none'; frame-ancestors 'none'
      X-Proxy-Cache-Status: MISS
      Via: 1.1 google
      Cache-Control: public,max-age=90
      Alt-Svc: clear
    Length: 769 [text/xml]
    Saving to: ‘update.xml’
    
         0K                                    100% 17.0M=0s
    
    2025-02-08 00:47:17 (17.0 MB/s) - ‘update.xml’ saved [769/769]
    
    Got this response:
    <?xml version="1.0"?>
    <updates>
        <update actions="showURL" appVersion="142.0" buildID="20250207232657" detailsURL="https://www.mozilla.org/en-CA/firefox/142.0/releasenotes/" displayVersion="142.0 Beta 5" openURL="https://www.mozilla.org/en-CA/firefox/142.0beta/whatsnew/?oldversion=%OLD_VERSION%&amp;utm_medium=firefox-desktop&amp;utm_source=update&amp;utm_campaign=142.0beta" type="minor">
            <patch type="complete" URL="https://ftp.stage.mozaws.net/pub/firefox/candidates/142.0b5-candidates/build1/update/linux-x86_64/en-CA/firefox-142.0b5.complete.mar" hashFunction="sha512" hashValue="657e9e6b802bd879428dd608924198018f690db28afedbf42b964835571ae4dcd692559f93c4da82ac532b74e97bf9d25fb4041c1e8df63717c1e26fd28c37b9" size="69608506"/>
        </update>
    </updates>
    
    Retrieving 'https://ftp.stage.mozaws.net/pub/firefox/candidates/142.0b5-candidates/build1/update/linux-x86_64/en-CA/firefox-142.0b5.complete.mar' from cache...

Log summary
^^^^^^^^^^^

Update verify performs some *very* basic log analysis and summary which is printed after all tests have been run. For a successful run, we expect to see:

.. code-block:: text

    Scanning log for failures and warnings
    --------------------------------------
    -------------------------
    All is well

A run with failures may, of course, have varied output, but one example of failure out is:

.. code-block:: text

    Scanning log for failures and warnings
    --------------------------------------
    TEST-UNEXPECTED-FAIL: [83.0 ru complete] check_updates returned failure for Darwin_x86_64-gcc3-u-i386-x86_64 downloads/Firefox 83.0b9.dmg vs. downloads/Firefox 136.0b1.dmg: 1
    TEST-UNEXPECTED-FAIL: [82.0 de complete] check_updates returned failure for Darwin_x86_64-gcc3-u-i386-x86_64 downloads/Firefox 82.0b1.dmg vs. downloads/Firefox 136.0b1.dmg: 1
    -------------------------
    This run has failed, see the above log

The square-bracketed string (eg: ``[83.0 ru complete]``) can be searched for in the log to find the full output from the test that failed.

diff-summary.log
================

Update verify tasks that have failed usually have a ``diff-summary.log`` in their artifacts. This file shows you all of the differences found for each update tested. In the diffs, ``source`` is an older version Firefox that a MAR file from the current release has been applied to, and ``target`` is the full installer for the current release.

Here's an example of a very alarming difference:

.. code-block:: text

   Found diffs for complete update from https://aus5.mozilla.org/update/3/Firefox/59.0/20180215111455/WINNT_x86-msvc/en-US/beta-localtest/default/default/default/update.xml?force=1

   Files source/bin/xul.dll and target/bin/xul.dll differ

In the above log, ``xul.dll`` is shown to be different between an applied MAR and a full installer. If we were to ship a release with a difference like this, partial MARs would fail to apply for many users in the *next* release. Usually a case like this represents an issue in the build system or release automation, and requires a rebuild. If you're not sure how to proceed, ask for help.

If no ``diff-summary.log`` is attached to the Task something more serious went wrong. You will need to have a look at the full log to investigate (see above).

Known differences
-----------------

There are no known cases where diffs are expected, so all task failures should be checked carefully.

See `bug 1461490 <https://bugzilla.mozilla.org/show_bug.cgi?id=1461490>`__ for the implementation of transforms to resolve expected differences.
