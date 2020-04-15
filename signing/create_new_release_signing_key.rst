Create a new release key to sign a new apk product
==================================================

The example product here is “rocket”
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before the release day: 1. SSH to a Linux (android) signing server 2.
Manually Create a new keystore dedicated to host the new cert[1]. For
future automation, passwords for both keystore and certificate must be
the same I usually use ``pwgen 80`` for the passphrase, scp down to my
laptop, scp up to the target server, unzip. secure wipe (srm, rm -P,
etc) the files on laptop afterwards. I created a keystore called
“rocket-jar” in /builds/signing/rel-key-signing-server/secrets. The
certificate in there has the alias “rocket”. Just like the release
certificate, I filled these values:
``CN=Release Engineering, OU=Release Engineering, O=Mozilla Corporation, L=Mountain View, ST=California, C=US``
I also needed to chmod 600 the keystore file and chown so it has the
same owner and group as other signing keystores. 3. Sign the APK[2] 4.
Give the APK back to the Rocket team.

Right after the first APK is signed: I. Store the passwords on the
private repo. II. Copy the keystore to the other signing servers.
Replication is usually done by archiving the keystore in a zip-encrypted
archive. The passphrase is usually 80 chars long III. Create two offline
backups of the keys[3].

For next releases: A. On the signing server, create a new signing
format, called something like “rocket-jar” B. Create new instances of
the signing server dedicated to that new format. This can be done by
either a new process on the same machine (but a different port) or by
creating a new machine. C. See whether the Focus team is ready to port a
part of their automation to Taskcluster. This would ensure the security
of the signing process.

[1]
https://mana.mozilla.org/wiki/display/RelEng/Signing#Signing-Jarsigning(APK)
[2]
https://developer.android.com/studio/publish/app-signing.html#sign-apk
[3] https://mana.mozilla.org/wiki/display/RelEng/Signing#Signing-Backups
