Manual iOS app upload to App Store Connect
==========================================

Note: Replace placeholders (APPLE_ID, APP_SPECIFIC_PASSWORD, /path/to/Client.ipa) in any command.

----

First create an App-Specific Password (Only if using CLI options)

- Go to https://id.apple.com and sign in.
- Account > Security > App-Specific Passwords > Generate Password. Save the password, and make sure to delete it after use.

----

Get the app bundle

- Download the `Client.ipa` artifact from the Bitrise build that produced the release (or the promote task created in ShipIt).

----

Upload options:

1. altool (simple CLI - deprecated, but still works and is available in XCode):

.. code-block:: bash
    xcrun altool --upload-app -f /path/to/Client.ipa -t ios --verbose -u "<YOUR APPLE ID EMAIL>" -p "<YOUR APP PASSWORD>"

2. iTMSTransporter (might require installing):

    Test if it is included in XCode tooling with `xcrun iTMSTransporter --help`. If you see an error, you might need to install it manually.
        If included, the app can be uploaded with the command:

        .. code-block:: bash

            xcrun iTMSTransporter -m upload -u "APPLE_ID" -p "APP_SPECIFIC_PASSWORD" -f /path/to/Client.ipa -v detailed -itc_provider MozillaCorporation

        Install iTMSTransporter if not already installed:

        - Download installer from https://help.apple.com/itc/transporteruserguide/en.lproj/static.html
        - Make sure it can be run with `/usr/local/itms/bin/iTMSTransporter --help`

        Upload the app with the command:

        .. code-block:: bash

            /usr/local/itms/bin/iTMSTransporter -m upload -u "APPLE_ID" -p "APP_SPECIFIC_PASSWORD" -f /path/to/Client.ipa -v detailed -itc_provider MozillaCorporation

3. Transporter App (GUI):

- Download from the Mac App Store: https://apps.apple.com/us/app/transporter/id1450874784?mt=12
- Open the app and sign in with your Apple ID.
- Drag and drop the Client.ipa file into the app window and click "Deliver".

-----

Verify

After upload, confirm the build appears in `App Store Connect <https://appstoreconnect.apple.com/apps>`_ > Apps > Select the App you uploaded > TestFlight > Builds.
