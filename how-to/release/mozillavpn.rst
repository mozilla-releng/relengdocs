Mozilla VPN Release Process
===========================

`Mozilla VPN`_ is shipped in two parts, the client and addons.

The client is shipped on Windows, Mac and Linux, as well as Android and iOS.
Ensure you are in the ``#releaseduty`` channel in Matrix.

Windows and Mac Clients
-----------------------

Windows and Mac client relases are triggered via Shipit.

Promote a Build
~~~~~~~~~~~~~~~

You'll receive a ping in the ``#releaseduty`` channel in Matrix asking to
"promote a build" or "push a build to candidates". The request should include a
link to the commit they would like promoted.

1. Log in to `Shipit`_.
2. From the ``Releases`` dropdown, select ``Security -> New Release``.
3. Select ``mozilla-vpn-client`` as the product.
4. Choose the release branch + commit mentioned in the request. The branch
   should match ``releases/<version>``.
5. Create the release and navigate to ``Security -> Pending Releases``.
6. Trigger the ``promote-client`` phase. This will run beetmover tasks that
   uploads the signed builds to the `candidates directory`_ on
   archive.mozilla.org. The builds will be under the path with the following
   pattern: ``pub/vpn/candidates/<version>-candidates/build<buildId>/``
7. :ref:`vpn balrog`, making sure to use the ``FirefoxVPN: release-cdntest``
   channel.
8. Reply in-thread that the candidate builds are ready for testing.

Ship a Build
~~~~~~~~~~~~

You'll receive a ping in the ``#releaseduty`` channel in Matrix asking to
ship or release a build. The request should include a link to the commit they
would like promoted.

1. Login to `Shipit`_.
2. From the ``Releases`` dropdown, select ``Security -> Pending Releases``.
3. Find the corresponding release that was created for the ``promote-client``
   phase.
4. Trigger the ``ship-client`` phase. This will run a beetmover task that
   copies the signed builds from candidates, over to the `releases directory`_
   on archive.mozilla.org.
5. :ref:`vpn balrog`, making sure to use the ``FirefoxVPN: release`` channel.
6. Reply in-thread in the ``#releaseduty`` channel that
   the release has been shipped on Windows and Mac.

.. _vpn balrog:

Update Balrog
~~~~~~~~~~~~~

Once the builds are on ``archive.mozilla.org``, you'll need to update the
``FirefoxVPN: release-cdntest`` channel on `Balrog`_ to point at them.

1. Create the release. It's usually easiest to copy/paste the previous release.

   a. Set the release name to ``FirefoxVPN-<version>``.
   b. Set the channel. Use ``FirefoxVPN: release-cdntest`` for the candidate builds.
      Use ``FirefoxVPN: release`` for the actual release.
   c. Update the URLs.
   d. Update the sha512 hashes, you'll need to download the binaries and
      compute them manually. Make sure the files are ``gunzip``'ed first
      (downloading via browser is safe way to ensure this).
   e. Update the version in the name and version fields.

2. Update the default rule to point to the new release.

Required Releases
`````````````````

From time to time, you may be asked to create a "required" release. This means
that the client will force users to update to the newer version (normally they
would have the option to ignore the update prompt). Required releases should be
created *in addition* to the release you created in the previous step.

1. Create the required release by copy/pasting the previous release blob except:

   a. Append ``-Required`` to the release name (both in Balrog and in the
      release blob).
   b. Change the ``required`` field to ``true``.
2. Update or create the appropriate rules to point to this release. It will
   likely be the case that only certain platforms or version numbers will want
   to use this release, so be sure to work with the VPN team to determine what
   exactly is desired.

Addons
------

Addons are shipped independently from the main client, they are akin to
Firefox's "system addons". They live in the main repo and are not to be
confused with web extensions (they use a custom format to VPN).

Addons releases are also managed via Shipit.

Promote Addons
~~~~~~~~~~~~~~

1. Login to `Shipit`_.
2. From the ``Releases`` dropdown, select ``Security -> New Release``.
3. Select ``mozilla-vpn-addons`` as the product.
4. Choose the ``main`` branch + commit mentioned in the request. Addons should
   always be released off of the ``main`` branch. If a branch other than
   ``main`` is requested, please verify that this is intentional and not an
   oversight.
5. Create the release and navigate to ``Security -> Pending Releases``.
6. Trigger the ``promote-addons`` phase. This will create beetmover tasks that
   upload the addons plus the manifest to the `addons candidates
   directory`_. The path will have a pattern like:
   ``pub/vpn/addons/candidates/<buildId>``
7. Reply in-thread that the candidate addons are ready for testing.

.. warning::

   Addons do not use version numbers and instead use the build date as their
   version. Shipit is unable to handle this scenario, so will display the
   client version instead. Please ignore this version number for the addons,
   and keep a mental note of which build number in Shipit corresponds to which
   build date in the release tasks.

Ship Addons
~~~~~~~~~~~

1. Login to `Shipit`_.
2. From the ``Releases`` dropdown, select ``Security -> Pending Releases``.
3. Find the corresponding release that was created for the ``promote-addons``
   phase.
4. Trigger the ``ship-addons`` phase. This will run beetmover tasks that copy
   the addons and signed manifest from candidates, over to the `addons releases
   directory`_ on archive.mozilla.org. The files will be uploaded to two
   locations:

   a. ``pub/vpn/addons/releases/<buildId>``
   b. ``pub/vpn/addons/releases/latest``

5. Reply in-thread in the ``#releaseduty`` channel that
   the release has been shipped on Windows and Mac.

Linux Client
------------

The Linux client is shipped via `launchpad`_, credentials are in Releng SOPS
under ``ubuntu-store.yml``.

.. note::

   For now we are still using builds generated by Github Actions, but will hopefully
   be switching to the Taskcluster builds shortly.

1. Ensure that ``publish`` is disabled in the `edit section of launchpad`_.
   This will ensure we don't accidentally ship the builds that are uploaded
   immediately.
2. Find the ``Sources.zip`` artifact from Github Actions. Ideally this will be
   linked by someone from VPN but if not:

   a. Click the ``Actions`` tab in Github.
   b. Click ``PPA Automated Releases`` workflow on the left.
   c. Under the branch filter, type in the version tag (e.g ``v2.10.0``).
   d. Click the task and download the ``Sources.zip`` at the bottom.

3. Extract the zip to a temporary directory:

   .. code-block:: bash

      $ unzip -d vpn_release Sources.zip
      $ cd vpn_release

4. Run a docker container to perform the signing:

   .. code-block:: bash

      export RELENG_GPG_KEYCHAIN=/path-to/releng-secrets-global/keys/mozillavpn-launchpad-gpg
      docker run --rm -it -v $(pwd):/packages -v $RELENG_GPG_KEYCHAIN:/keychain --entrypoint /bin/bash ubuntu:latest -i

5. When inside the container, run the following commands:

   .. code-block:: bash

      apt update && DEBIAN_FRONTEND=noninteractive apt install -y devscripts dput rsync
      rsync -av /keychain/ /keychain2/
      export GNUPGHOME=/keychain2
      cd /packages
      # have the passphrase at hand in keys/mozillavpn-launchpad-gpg.passphrase
      # for the next command for signing
      debsign -k Release --re-sign *.dsc *.buildinfo *.changes
      dput ppa:mozillacorp/mozillavpn mozillavpn*.changes

   An email will be sent by lauchpad to release+ubuntu-store@mozilla.com.

   If ``dput`` complains about the package had already been uploaded, then delete all files ``*.ppa.upload`` and try again.

   If the build fails for some reason (i.e.: GPG key rotated), and the server complains the package has already been
   uploaded, then ``dput`` can be run with ``-f`` to force the upload/override.

6. The build should eventually show up on `launchpad`_. You can also
   `watch the state of the builds here`_.

   a. If the builds fail without a log, it could indicate an infra issue. Retrying the build (button in launchpad) is then recommended.

7. Once the builds are successful, open the `edit section of launchpad`_ and
   check the ``Publish`` box. Click ``Save``.
8. After the releases have been shipped and verified, go back and disable
   ``Publish`` again.

Android and iOS Clients
-----------------------

Releng is not involved with the mobile release process.

.. _Shipit: https://shipit.mozilla-releng.net/
.. _Mozilla VPN: https://github.com/mozilla-mobile/mozilla-vpn-client
.. _release promotion action:
.. _candidates directory: https://archive.mozilla.org/pub/vpn/candidates/
.. _RELENG-797: https://mozilla-hub.atlassian.net/browse/RELENG-797
.. _releases directory: https://archive.mozilla.org/pub/vpn/releases/
.. _Balrog: https://balrog.services.mozilla.com/
.. _launchpad: https://launchpad.net/~mozillacorp/+archive/ubuntu/mozillavpn
.. _edit section of launchpad: https://launchpad.net/~mozillacorp/+archive/ubuntu/mozillavpn/+edit
.. _watch the state of the builds here: https://launchpad.net/~mozillacorp/+archive/ubuntu/mozillavpn/+builds?build_text=&build_state=all
.. _addons candidates directory: https://archive.mozilla.org/pub/vpn/addons/candidates/
.. _addons releases directory: https://archive.mozilla.org/pub/vpn/addons/releases/
