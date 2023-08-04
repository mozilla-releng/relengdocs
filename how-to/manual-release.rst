.. _manual-release:

Manually submit a release with the Ship It API
==============================================

Releases are typically kicked off with the Ship It UI. At times (usually if there's bustage preventing the Ship It UI from working), it can be necessary to kick off a release through the API directly.

Doing so is a fairly straightforward procedure, as documented below:

#. Gather the information required to submit the Release (if you're unsure what these should be, try querying https://shipit-api.mozilla-releng.net/releases for values used by previous releases, or asking for help):

    * Branch
    
    * Build Number

    * Product

    * Repo URL

    * Revision

    * Version

#. Copy your Access Token out of Local Storage.

    #. Open https://shipit.mozilla-releng.net/ in Firefox

    #. Ensure you are logged into Ship It

    #. Open the Developer Tools window (F12)

    #. Go to the "Storage" tab

    #. Expand the "Locale Storage" entry on the left, and click on the "https://shipit.mozilla-releng.net/" entry.

    #. Click on the "react-auth0-session" key that shows up

    #. Expand the "authResult" key on the right

    #. Right click on the "accessToken" on the right and click "Copy"

    #. Paste this value somewhere private, and clear your clipboard. It should show up as a key and value in the form of 'accessToken:"xxxxxxxxxx"'. The "xxxxxxxxxx" part is your access token, and will be used in the next step.

#. Submit the Release with the following curl command, substituting in the information you gathered and access token where appropriate::

    curl 'https://shipit-api.mozilla-releng.net/releases' -X POST \
    -H 'authorization: Bearer xxxxxxx' -H 'content-type: application/json' \
    --data-raw '{"branch":"$BRANCH","build_number":$BUILD_NUMBER,"product":"$PRODUCT","repo_url":"$REPO_URL","revision":"$REVISION","version":"$VERSION"}'

For example, the following command was used to kick off a Firefox Android release::

    curl 'https://shipit-api.mozilla-releng.net/releases' -X POST \
    -H 'authorization: Bearer xxxxxxx' -H 'content-type: application/json' \
    --data-raw '{"branch":"releases_v117","build_number":1,"product":"firefox-android","repo_url":"https://github.com/mozilla-mobile/firefox-android","revision":"e5f7a268cf2543918ff80697f37e85bdcff849c9","version":"117.0b1"}'

Once submitted, the release should show up on https://shipit.mozilla-releng.net/ (just as it would if submitted through the UI), and the appropriate Phase can be run as usual.

