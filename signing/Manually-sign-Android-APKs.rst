Manually Sign Android APKS
==========================

Currently, two products may need manually signing:

-  Firefox Rocket
-  Firefox Focus for Android. :warning: This product has two APKs: one
   is Focus, the other for the German-speaking population: Klar.

Requirements
------------

Google Play refuses non-optimized APKs. The signature changes the
structure of the APK archive, which breaks the Zip optimization.

1. Install the latest Android SDK to get the build tools.

   -  MacOSX: ``brew cask install android-sdk`` (requires
      ``brew tap caskroom/cask``)

      -  then run ``sdkmanager --list`` and install build-tools,
         e.g. ``sdkmanager 'build-tools;27.0.3'``. It'll show up in
         e.g. ``/usr/local/share/android-sdk/build-tools/27.0.3/zipalign``

   -  Ubuntu: ``apt install android-sdk``
   -  Other: `Install Android
      Studio <https://developer.android.com/studio/index.html#Other>`__

First Steps
-----------

1. ``ssh signing4.srv.releng.scl3.mozilla.com``

2. Change to the ``cltsign`` user:

   .. code:: sh

      sudo su - cltsign

To sign an APK
--------------

You will need to repeat this for each APK, feel free to optimize by
downloading all at once, just be careful of filenames when copy/pasting
commands.

1. Download unsigned APK(s).

   -  Right-click the attachment in bugzilla and click ‘Copy Link
      Location'
   -  ``wget -O unsigned.apk <pasted url>``

2. Set environment variables:

   -  For Focus/Klar:

      .. code:: sh

         keystore='/builds/signing/rel-key-signing-server/secrets/focus-jar'
         alias='focus'

   -  For Rocket:

      .. code:: sh

         keystore='/builds/signing/rel-key-signing-server/secrets/rocket-jar'
         alias='rocket'

3. Look up the right keystore password in the releng private repo

   -  Focus/Klar is under the name ``signing-server-focus``
   -  Rocket is under the name ``signing-server-rocket``

4. ``jarsigner -keystore "$keystore" unsigned.apk "$alias"`` You'll be
   asked for the password in the previous step. The Klar APK uses the
   same certificate alias/password as ``focus``. You'll also get an
   expected warning:

   ::

      Warning:
      No -tsa or -tsacert is provided and this jar is not timestamped. Without a timestamp, users may not be able to validate this jar after the signer certificate's expiration date (2044-10-25) or after any future revocation date.

5. ``mv unsigned.apk signed.apk``

6. Verify signatures:
   ``jarsigner -verify -verbose -keystore "$keystore" signed.apk "$alias"``

7. If your product has several APKs, repeat the previous steps. You may
   want to give the files more useful names, such as
   ``app-rocket-webkit-release-signed.apk``

After all the signing
---------------------

1. Fetch signed APK(s) on your local machine. You will need to copy the
   files to your own user account in order to ``scp`` them, as you can't
   directly reach the ``cltsign`` user.

2. Optimize the APKs for Google Play, and verify. For each APK:

   .. code:: sh

      zipalign -v 4 signed.apk signed-aligned.apk
      zipalign -c -v 4 signed-aligned.apk

3. Attach the signed and aligned APKs to the bug using the 'attach file'
   feature in bugzilla.

Troubleshooting
---------------

Can't sign APKs
~~~~~~~~~~~~~~~

Sometimes, APKs aren't correctly formatted. For instance, CI may have
already signed an APK with a dev key. In this case, you may see:

.. code:: sh

   $ jarsigner -verbose -keystore "$keystore" unsigned.apk "$alias"
   Enter Passphrase for keystore:
   jarsigner: unable to sign jar: java.util.zip.ZipException: invalid entry compressed size (expected 34549 but got 35093 bytes)

The fix is just to strip the signature from the package:

.. code:: sh

   $ zip -d unsigned.apk META-INF/\*
   deleting: META-INF/CERT.RSA
   deleting: META-INF/CERT.SF
   deleting: META-INF/MANIFEST.MF

Then you can resume signing.

Future
------

We already have a github repo with taskcluster release builds. It's not
trivial, but it's possible we could add CoT and auto-sign these release
builds.
