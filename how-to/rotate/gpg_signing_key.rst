How to rotate the Firefox Release signing GPG Key
=================================================

This is a rough guide, and is likely going to be out of date every time we have to rotate the keys. It is likely you will have to take different or additional steps than described here. It's always a good idea to look at the most recent rotation bug (like https://bugzilla.mozilla.org/show_bug.cgi?id=1703397) before getting started.

When
~~~~
You should start this process at least a month prior to the current key expiring. Because this work spans multiple teams and requires multiple deployments, there's usually a bit of lead time involved, and you'll want some slack time in case something goes wrong.

Process
~~~~~~~
At a high level, the process is as follows:

1) Generate a new signing subkey
2) Publish the new public key
3) Import the new private key into autograph
4) Test the new key in adhoc-signing
5) Update the public key in a few places
6) Start signing with the new private key

Here's slightly more detail on each step

Generate a new signing subkey
-----------------------------
This is documented on https://mozilla-hub.atlassian.net/wiki/spaces/SECURITY/pages/27168879/Releng+Product+Signing+GnuPG+key+generation+and+handling.

The most important end result of this process will be a new private signing subkey that has been deployed to `Autograph`_, a new public signing subkey, and access to the private key through a new set of credentials that you will be provided.

.. _Autograph: https://github.com/mozilla-services/autograph

Publish the new public key
--------------------------
The new key needs to be published on keys.openpgp.org. Be sure to "verify" the key after publishing, by having them send an e-mail link to click on, to make sure users will see an identity associated with it (otherwise it's useless).

A blog post like https://blog.mozilla.org/security/2019/06/13/updated-firefox-gpg-key/ should also be made.

Import the new private key into autograph
-----------------------------------------
You will need to send the new private key and its passphrase to an autograph team member. They will handle importing it into autograph, and creating new credentials (if necessary). These days, it's most likely preferable to have the same credentials be used, and have the GPG key accessible through a new ``keyid`` available to those credentials. (This avoids the need to update signingscript secrets and helm charts.)

Test the new key in adhoc-signing
---------------------------------

The new signing subkey will be deployed to the production instance of `Autograph`_, which means it must be tested through a production worker and repository. The best and safest way to do this is against the `Adhoc Signing`_ repository - which will not impact any users or developers if something goes wrong. You can do this as follows:

1) Update the `GPG_PUBKEY_PATH` entry for `firefoxci-adhoc-3` in the `scriptworker-scripts` repository.

    a) Create a new gpg keyring and import the current key::

        mkdir new-keyring
        gpg --homedir new-keyring --import current.key

    b) Add the new public key to the keyring::

        gpg --homedir new-keyring --import new-public.key

    c) Export *all* the keys to a new armored file::

        gpg --homedir new-keyring --export --armor > new.key

    d) Add the header from the existing KEY file to `new.key`, with the new sub key information (generated with e.g. `gpg --show-key --list-options show-unusable-subkeys < new.key`). For example, in the 2023 rotations we added the following (the last line is the new subkey information)::

        This file contains the public PGP key that is used to sign builds and
        artifacts of Mozilla projects (such as Firefox and Thunderbird).

        Please realize that this file itself or the public key servers may be
        compromised.  You are encouraged to validate the authenticity of these keys in
        an out-of-band manner.

        Mozilla users: pgp < KEY

        pub   rsa4096 2015-07-17 [SC]
              14F26682D0916CDD81E37B6D61B7B526D98F0353
        uid           [  full  ] Mozilla Software Releases <release@mozilla.com>
        sub   rsa4096 2015-07-17 [S] [expired: 2017-07-16]
        sub   rsa4096 2017-06-22 [S] [expired: 2019-06-22]
        sub   rsa4096 2019-05-30 [S] [expires: 2021-05-29]
        sub   rsa4096 2021-05-17 [S] [expires: 2023-05-17]
        sub   rsa4096 2023-05-05 [S] [expires: 2025-05-04]

    e) Add new.key to signingscript and point the `firefoxci-adhoc-3` pool's `GPG_PUBKEY_PATH` variable at it.

    f) Open a Pull Request with the changes; wait for it to get merged.

2) Update the GPG username and password for `firefoxci-adhoc-3` in the relengworker SOPS repository (if necessary).
3) Deploy production scriptworkers to pick up the changes you made above.
4) Open a PR with a new signing manifest in the `Adhoc Signing`_ repository that will sign with GPG (note: when it does a test signing as part of opening a PR, it will not be using the new keys, because PRs use dep certs).
5) Get your PR reviewed and merged.
6) Use the `Promote an Adhoc Signature` action to kick off signing for your new manifest. *This* should sign successfully with the new subkey.
7) Verify the `KEY` file and detached signature that the task publishes. This will look something like::

    # Download the file that was signed, the detached signature, and the `KEY` to your local machine
    # Create a new keyring and import the published KEY file
    mkdir new
    gpg --homedir new --import KEY
    # Verify the detached signature
    gpg --homedir new --verify *.asc
    # You should see output like:
    # gpg: Good signature from "Mozilla Software Releases <release@mozilla.com>"

You can also find an example of the adhoc signing manifest `in this PR`_. If that signing manifest still exists in the repository, you can even skip steps 4 and 5, and promote that manifest in step 6 instead.

.. _Adhoc Signing: https://github.com/mozilla-releng/adhoc-signing
.. _Autograph: https://github.com/mozilla-services/autograph
.. _KEY file we publish: https://archive.mozilla.org/pub/firefox/releases/111.0/KEY
.. _in this PR: https://github.com/mozilla-releng/adhoc-signing/pull/165


Update the public key in a few places
-------------------------------------
We publish our public key in a couple of places, and store it in others to verify some of our own signatures. Specifically, at least the following will need to be updated:

* The reference-browser repository Eg: https://github.com/mozilla-mobile/reference-browser/pull/2326

You may discover other places that need to be updated that aren't in this list! Please update this doc if you do.

Start signing with the new private key
--------------------------------------

Now that you've verified that the autograph credentials work, and that the gpg signatures produced are correct, you can roll it out to the remaining signingscript pools. This will look nearly identical to what you did when testing adhoc-signing.. This must be done for each signing pool that uses our primary GPG key. At the time of writing this is the following (not including the adhoc one you just updated)::

   firefoxci-gecko-3 prod
   firefoxci-comm-3 prod
   firefoxci-mobile-3 prod
   firefoxci-app-services-3 prod
   firefoxci-glean-3 prod
   firefoxci-adhoc-3 prod

**Do not take this list as complete.** Things have likely changed since these instruction were written. You should inspect both files and make a complete list of everything using the previous subkeys.

Take caution to avoid doing this if there are releases in flight. If you do, files from the same release will get signed with different keys. This doesn't break anything, but it does cause confusion.
