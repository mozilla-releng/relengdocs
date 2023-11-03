Rotate Github App Private Keys
==============================

Releng uses Github Apps for authentication in a variety of places. This page
outlines how to rotate the private keys associated with a Github App that are
used to `generate an app installation token`_.

Steps to Rotate
---------------

1. Open https://github.com/organizations/mozilla-releng/settings/apps and click
   ``Edit`` next to the app you are rotating.
2. Scroll down to the ``Private Keys`` section and click the ``Generate a
   private key`` button. This will prompt a download of the private key and
   associate the public key with the app.
3. Verify the downloaded private key matches the public key in Github by
   `following these steps`_.
4. Update the appropriate places with the new private key:

   a. ``releng-treescript`` - Key should go in relengworker SOPS (base64 encoded). E.g:
      ``cat path/to/private-key.pem | base64 -w0 | xclip``
5. Back in the app settings, press ``Delete`` on the old key(s) you are rotating.

.. _generate an app installation token: https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app
.. _following these steps: https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/managing-private-keys-for-github-apps#verifying-private-keys
