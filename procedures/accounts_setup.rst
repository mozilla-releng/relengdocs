Accounts Setup
==============

Here is a list of accounts and access needed to be successful in Release Engineering

General:
 * `JIRA <https://jira.mozilla.com/projects/RELENG/issues>`_ - via SSO, but need to add user for RELENG project
 * `Commit Access <https://www.mozilla.org/en-US/about/governance/policies/commit/access-policy/>`_ - fill out form, file bug
 * Bugzilla (via SSO)
 * Phabricator (via SSO)
 * Github
 * `Mozilla VPN <https://mana.mozilla.org/wiki/pages/viewpage.action?pageId=30769829>`_
 * ssh keys?
 * GPG keys?
 * 2FA?

Release Duty:
 * `Release duty rotation <https://wiki.mozilla.org/Release_Management/Release_owners>`_

Mailing Lists:
 * follow instructions at `day1 <https://wiki.mozilla.org/ReleaseEngineering/Day_1_Checklist#Communication>`_

LDAP Permissions:
 * for release duty: `sample bug <https://bugzilla.mozilla.org/show_bug.cgi?id=1681190>`_

Setting up a GPG key
--------------------

A GPG key will be needed for `SOPS`_ (see below) as well as verifying Git commits. Follow
`these instructions <https://mana.mozilla.org/wiki/display/SD/Generating+a+GPG+Public+Key>`_
to create a new GPG key.

Make sure you follow the steps to upload it to `keys.openpgp.org <https://keys.openpgp.org>`_
and add your fingerprint to `login.mozilla.com <https://login.mozilla.com>`_.

Add GPG key to Github and Git
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also use your GPG key to verify commits. This is usually optional, but
is a requirement in some repositories.

1. Follow `these instructions to add your key to Github`_
2. Follow `these instructions to register your key with Git`_

.. _these instructions to add your key to Github: https://docs.github.com/en/authentication/managing-commit-signature-verification/adding-a-new-gpg-key-to-your-github-account
.. _these instructions to register your key with Git: https://docs.github.com/en/authentication/managing-commit-signature-verification/telling-git-about-your-signing-key


Setting up SOPS
---------------

`SOPS`_ is a way to track secrets in a Git repository and securely share them
with the rest of the team. You'll need to set this up to access credentials and
keys needed for various services Release Engineering uses or administers.

1. Install the `latest version of SOPS <https://github.com/mozilla/sops/releases>`_
2. Install the `Google Cloud SDK <https://cloud.google.com/sdk/docs/downloads-interactive>`_

   a. Follow the interactive instructions for your platform
   b. When prompted, login to your Mozilla associated Google account
   c. When prompted for a project, choose ``moz-fx-releng-secrets-global``

3. Run the following command:

.. code-block:: shell

   # will clone into $CWD, you can pass a directory after `releng-secrets-global` to clone elsewhere 
   $ gcloud source repos clone releng-secrets-global --project=moz-fx-releng-secrets-global

4. If you set up your GPG key as per the previous section, and someone has re-encrypted the secrets in SOPS with it, you should now be able to decrypt the files:

.. code-block:: shell

   $ cd releng-secrets-global
   # piping into your editor keeps the secrets out of your shell's scrollback buffer
   $ sops -d passwords/coderpad.yml | $EDITOR

.. _SOPS: https://github.com/mozilla/sops
