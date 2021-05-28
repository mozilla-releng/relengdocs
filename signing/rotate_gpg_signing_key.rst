How to rotate the Firefox Release signing GPG Key
=================================================

This is a rough guide, and is likely going to be out of date every time we have to rotate the keys. It is likely you will have to take different or additional steps than described here. It's always a good idea to look at the most recent rotation bug (like https://bugzilla.mozilla.org/show_bug.cgi?id=1703397) before getting started.

When
~~~~
You should start this process at least a month prior to the current key expiring. Because rotation involves access to the offline master keychain, there's usually a bit of lead time involved.

Process
~~~~~~~
At a high level, the process is as follows:
1) Generate a new signing subkey
2) Publish the new public key
3) Import the new private key into autograph
4) Update the public key in a few places
5) Start signing with the new private key

Here's slightly more detail on each step

Generate a new signing subkey
-----------------------------
This is documented on https://mana.mozilla.org/wiki/display/SECURITY/Releng+Product+Signing%3A+GnuPG+key+generation+and+handling.

Publish the new public key
--------------------------
The new key needs to be published on keys.openpgp.org. Be sure to "verify" the key after publishing, by having them send an e-mail link to click on, to make sure users will see an identity associated with it (otherwise it's useless).

A blog post like https://blog.mozilla.org/security/2019/06/13/updated-firefox-gpg-key/ should also be made.

Import the new private key into autograph
-----------------------------------------
You will need to send the new private key and its passphrase to an autograph team member. They will handle importing it into autograph, and creating new credentials (if necessary).

Update the public key
---------------------
We publish our public key in a couple of places, and store it in others to verify some of our own signatures. Specifically, at least the following will need to be updated:
* The `KEY` file in the signingscript config in CloudOps` repo. (Private repo, purposely not linked here)
* Fenix and reference-browser's repositories. Eg: https://github.com/mozilla-mobile/fenix/pull/19691 and https://github.com/mozilla-mobile/reference-browser/pull/1610

Start signing with the new private key
--------------------------------------
This will probably involve changing the signingscript secrets to use new autograph credentials that are associated with the new key, and then deploying signingscript.
