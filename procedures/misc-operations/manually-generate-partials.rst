Based on
https://wiki.mozilla.org/ReleaseEngineering/How_To/Generate_partial_updates

When?
=====

Under some circumstances, users may be `stranded on old
releases <https://telemetry.mozilla.org/update-orphaning/>`__. In this
case, Release Management might ask to generate a partial update from
this old release to the most current version (like in `bug
1347030 <https://bugzilla.mozilla.org/show_bug.cgi?id=1347030>`__).

Assumptions: \* the request is for the release channel \* all locales
are being generated, possibly only some of the platforms (which are
win32 and win64 in this tutorial)

How?
====

1. build/tools changes
----------------------

.. code:: sh

   export FROM_VERSION='47.0.2'  # Change this
   export TO_VERSION='53.0'  # Change this
   export TO_BUILD='6'   # Change this
   export TO_VERSION_UNDERSCORE = ${TO_VERSION//./_} # Example: 53_0

   wget
   "https://hg.mozilla.org/releases/mozilla-release/raw-file/FIREFOX_${TO_VERSION_UNDERSCORE}_RELEASE/browser/locales/shipped-locales"
   PERL5LIB=tools/lib/perl perl tools/release/patcher-config-bump.pl \
     -c tools/release/patcher-configs/mozRelease-branch-patcher2.cfg \
     -p firefox -r Firefox -v "$TO_VERSION" -a "$TO_VERSION" -o "$FROM_VERSION" -b "$TO_BUILD" \
     -f archive.mozilla.org -d download.mozilla.org -l shipped-locales --partial-version "$FROM_VERSION" \
     --platform linux --platform linux64 --platform macosx64 --platform win32 --platform win64

   python tools/scripts/build-promotion/create-update-verify-config.py \
     --config tools/release/patcher-configs/mozRelease-branch-patcher2.cfg \
     --platform win32 --update-verify-channel release-localtest \
     --output tools/release/updates/release-firefox-win32.cfg \
     --archive-prefix https://archive.mozilla.org/pub \
     --previous-archive-prefix https://archive.mozilla.org/pub \
     --product firefox --balrog-url https://aus5.mozilla.org --build-number "$TO_BUILD"

   python tools/scripts/build-promotion/create-update-verify-config.py \
     --config tools/release/patcher-configs/mozRelease-branch-patcher2.cfg \
     --platform win64 --update-verify-channel release-localtest \
     --output tools/release/updates/release-firefox-win64.cfg \
     --archive-prefix https://archive.mozilla.org/pub \
     --previous-archive-prefix https://archive.mozilla.org/pub \
     --product firefox --balrog-url https://aus5.mozilla.org --build-number "$TO_BUILD"

   cd tools/

   # Edit release/updates/release-firefox-win32.cfg and release/updates/release-firefox-win64.cfg to only contain the line about $FROM_VERSION

   hg commit
   hg push -r . review   # Ask for a review

   # Once review is passed, retag the following:
   hg tag -f -r . "FIREFOX_${TO_VERSION_UNDERSCORE}_RELEASE_RUNTIME" "FIREFOX_${TO_VERSION_UNDERSCORE}_BUILD${TO_BUILD}_RUNTIME"

   hg push -r .^  # Actual changes
   hg push -r .    # Tags

2. Update the balrog blobs and generate taskgraph
-------------------------------------------------

1. Clone the current production blob and rename it to ``*-prod``. Make
   the production rule to this new blob.
2. Then, you need to make some changes on the blog you just copied,
   otherwise the update verify tests will fail.
3. Download the release blob make these changes:
   ``["fileUrls"]["release-localtest"]["partials"].append("Firefox-${FROM_VERSION}-build${FROM_BUILD}": "http://archive.mozilla.org/pub/firefox/candidates/${TO_VERSION}-candidates/build${TO_BUILD}/update/%OS_FTP%/%LOCALE%/firefox-${FROM_VERSION}-${TO_VERSIONs}.partial.mar")``
4. Upload the new blob and make the release-localtest rule point to this
   new blob.
5. 

.. code:: sh

   ssh buildbot-master85.bb.releng.scl3.mozilla.com
   sudo su - ctlbld
   mkdir bug-xxxxxx && cd bug-xxxxxx
   curl --location https://bugzilla.mozilla.org/attachment.cgi?id=8818876 > partials.tar.gz
   tar xvf partials.tar.gz
   cd partials
   cd partials-47.0.2-50.1.0/

   # Modify runme.py to point to $TO_VERSION
   # Fill the creds in config.yml
   source /builds/releaserunner/bin/activate
   python runme.py

   # If the graph is printed out, uncomment the last line of runme.py
   python runme.py

3. Update balrog blobs (one more time) and bouncers
---------------------------------------------------

1.  Manually add the bouncer entries, which means:
2.  Create a new product called
    ``Firefox-${TO_VERSION}-Partial-${FROM_VERSION}``. Don’t include the
    build numbers in the name. Build numbers are for ``*-cdntest``
    channels, only. For instance:
    https://bounceradmin.mozilla.com/admin/mirror/product/6993/
3.  Create 1 location per platform for this new product. Ask for a
    review, because typos can happen. (Corrected) example:
    https://bounceradmin.mozilla.com/admin/mirror/location/?product__id__exact=6993
4.  Resolve the human decision of the graph.
5.  Wait for https://bounceradmin.mozilla.com/stats/locations/?p=6993 to
    show some products (replace the ID of the product by yours)
6.  Manually test out the bouncer. Change this link
    http://download.mozilla.org/?product=firefox-:math:`{TO_VERSION}-partial-`\ {FROM_VERSION}&os=win&lang=fr
    with your product name and all the locations you created. That’s
    case insensitive.
7.  On balrog, perform this addition on the release (non ``*-prod``)
    blob,
    ``["fileUrls"]["*"]["partials"].append("Firefox-${FROM_VERSION}-build${FROM_BUILD}": "http://download.mozilla.org/?product=firefox-${TO_VERSION}-partial-${FROM_VERSION}&os=%OS_BOUNCER%&lang=%LOCALE%")``.
    Manually change the ``${VARIABLES}``
8.  If you have a what’s new page blob on balrog
9.  Download the regular blob (the one just updated in step 6), which
    now contains all the partials.
10. Add the whatsnew bits to it, which is detailed in
    https://wiki.mozilla.org/Release:Release_Automation_on_Mercurial:Updates_through_Shipping#Set-up_whatsnew_page
    (Don’t forget to change the name)
11. Ask for another review.
12. You can now test out the balrog rule. In order to to so:
13. Go to the logs of one update verify job.
14. Copy one of URL, like:
    https://aus4.mozilla.org/update/3/Firefox/47.0.2/20161031133903/WINNT_x86-msvc-x86/eo/release-localtest/default/default/default/update.xml?force=1
15. Modify it to now point to release (and to aus5, which has a valid
    certificate):
    https://aus5.mozilla.org/update/3/Firefox/47.0.2/20161031133903/WINNT_x86-msvc-x86/eo/release/default/default/default/update.xml?force=1
16. See the new partial entry in the XML, for instance:
    ``<patch type="partial" URL="http://download.mozilla.org/?product=firefox-53.0-partial-47.0.2&os=win&lang=eo&force=1" hashFunction="sha512" hashValue="1f8a24ec43002477b21ffdc06cdbb7c885ebf57eecc08e45c31089ceac1a9e57cf9ec2c4becc638ec346335e5d84e9384f2503d61a259232151cb6e173126cce" size="42336047"/>``
17. Copy/paste the URL, just to make sure it’s a valid one.
