Day 1 checklist
===============

Welcome to Release Engineering!
This page is meant to get new hires, interns, or interested community members up to speed with the right software,
configurations, and communication channels to contribute effectively to the release engineering pipeline.

## Basic

The accounts get activated 1 day before joining so the manager of the team should drop a Slack message and an email to ensure comms are working properly.
Moreover, your manager should have already scheduled a 1x1 to go over things (welcoming doc, permanent weekly 1x1 timeslot) on Monday and another one on Friday to ensure week #1 went smoothly and learn about the painpoints.

## Accounts setup
Here is a list of accounts and access needed to be successful in Release Engineering.

### Bugzilla

Almost everything at Mozilla goes through Bugzilla. [Create a Bugzilla account](https://bugzilla.mozilla.org/createaccount.cgi) if you have not already.
You'll need a few tweaks to your account to get access to everything releng-related:
* Add privileges for bugzilla group releng confidential (Can be done by manager or bugzilla admin)
* Add your comms nickname & ldap username as `aliases` for your account
* log into bugzilla & follow links `Preferences` -> `Account Information`
* append the aliases, with a leading ':' and enclosed in brackets ('[]') to the "Real Name" field
* e.g.: `John Doe [:jdoe]`

The product to use is **"Release Engineering."** There are multiple possible components under that product, so take your best guess or ask for guidance from the team.

**TODO** - to revisit once we reorg Bugzilla in November 2022.

:warning: Please speak with your manager to be added to the [releng-security](https://bugzilla.mozilla.org/page.cgi?id=group_admins.html) confidential group.

### Misc

* SSO - we rely on [auth0](https://auth0.com/) across Mozilla for authentication and [LDAP](https://mana.mozilla.org/wiki/display/SYSADMIN/LDAP+Architecture) for authorization.
Once given LDAP and you have created a permanent password, you can use that to login to the [portal](https://sso.mozilla.com/). From SSO, you should have links to various services from email, calendar, slack, mana, etc.
* [https://login.mozilla.com/](https://login.mozilla.com/) is where you can change a number of authentication/authorization access bits that you have control over. Each todo in this section assumes you have access to this page.
* SSH - upload your public ssh key to [Login Portal](https://login.mozilla.com/ssh_keys_index), [GitHub](https://github.com/settings/keys). It is a good idea to generate a separate SSH keypair from your personal one or any other that you have created in the past and use that explicitly for Releng and upload that. Follow this [SSH guidelines](https://infosec.mozilla.org/guidelines/openssh#openssh-client) doc on how to generate, configure, and use your SSH key.
* GPG - We use gpg keys to share private information, secrets, and verify that the source came from someone we trust. Generate a keypair and upload your public key to [OpenPGP](https://keys.openpgp.org/) so others can find it. It would be really good if you could have other people sign your key, adding more trust that this key really belongs to you. You can use the the [GPG quickstart](https://mana.mozilla.org/wiki/display/SD/Generating+a+GPG+Public+Key) guide on mana or you can use the The [GNU Privacy Handbook](https://www.gnupg.org/gph/en/manual.html) for reference.
Also don't forget to add the fingerprint under [https://login.mozilla.com/](https://login.mozilla.com/) too. Moreover, you'll have to add your GPG key to Github and Git. This is usuaully optional but is a requirement in some repositories. Follow [these instructions to add your key to Github](https://docs.github.com/en/authentication/managing-commit-signature-verification/adding-a-new-gpg-key-to-your-github-account) and [these instructions to register your key with Git](https://docs.github.com/en/authentication/managing-commit-signature-verification/telling-git-about-your-signing-key) for more details.
* VPN - Many of our systems are behind a private network in addition to auth0. Follow the prompts to generate and download an openVPN certificate that you can use to import to your vpn client. See the instructions on how to [install and configure your VPN client](https://mana.mozilla.org/wiki/display/SD/VPN) and help choosing the right client for your platform. Note: macOS and Windows users should use [Viscosity](https://www.sparklabs.com/viscosity/). This application comes with a free 30 day trial. During your trial, your manager can help you create a JIRA ticket to get a Viscosity full license.
* MFA - More information on Multi-Factor-Authentication can be found in the [Login Portal](https://login.mozilla.com/duo/) which is what we use for LDAP/auth0 based logins. Follow [these](https://mana.mozilla.org/wiki/pages/viewpage.action?pageId=145590267) instructions to download the Duo Mobile app and set it up.
* Mercurial - Most development in releng (and at Mozilla writ-large) is stored in version control using [hg](http://mercurial.selenic.com/). There is an excellent step-by-step guide for setting up and using hg: [Mercurial for Mozillians](https://mozilla-version-control-tools.readthedocs.org/en/latest/hgmozilla/index.html). More information on this can be found in [here](https://firefox-source-docs.mozilla.org/contributing/vcs/mercurial.html) and [here](https://firefox-source-docs.mozilla.org/contributing/contribution_quickref.html).

## Phabricator

You will be granted access to this via SSO. Please ask your manager to be added to the following team reviewing aliases:
* [releng-reviewers](https://phabricator.services.mozilla.com/tag/releng-reviewers/)
* (optional) [taskgraph-reviewers](https://phabricator.services.mozilla.com/project/view/140/)

## Mercurial

The root webview of the Mozilla hg repositories is here: [hg.mozilla.org](https://hg.mozilla.org/) while most releng code lives in repos under [hg.mozilla.org/build](https://hg.mozilla.org/build).
Please fill out the [Commit Access form](https://www.mozilla.org/en-US/about/governance/policies/commit/access-policy/) and submit it via a bug on file such as [this](https://bugzilla.mozilla.org/show_bug.cgi?id=1734247). Make sure to include (comment) your SSH public key and request 2 peers to vouch for you.

There are 3 levels of commit access:
    * Level 1 access allows you to use the [Try Server](https://wiki.mozilla.org/ReleaseEngineering/TryServer) and setup user repos. As a new contributor, you should request this on day one.
    * Level 2 access is required to land code in the build and project repos. Once you have a proven track record of successful patches, you can ask your manager/mentor to vouch for your Level 2 access. Your manager/mentor can also land patches for you until you receive Level 2 access
    * Level 3 access is required to land code in [mozilla-central](https://hg.mozilla.org/mozilla-central) and its derived integration & release branches. At some point in your Mozilla contribution story, you may need Level 3 access but many contributors never do. Talk to your manager/mentor if you think you need this access. You should already have Level 2 access when you request Level 3

## Git & Github
Please file a bug similar to [bug 1726348](https://bugzilla.mozilla.org/show_bug.cgi?id=1726348) and include the following teams to be added. Ask for your manager to vouch in the bug for these changes. The teams you need to be added are:
1. [https://github.com/orgs/mozilla/teams/releng/members](https://github.com/orgs/mozilla/teams/releng/members)
2. [https://github.com/orgs/mozilla-releng/people](https://github.com/orgs/mozilla-releng/people)
3. [https://github.com/orgs/mozilla-releng/teams/releng/members](https://github.com/orgs/mozilla-releng/teams/releng/members)
4. [https://github.com/orgs/mozilla-mobile/teams/releng/members](https://github.com/orgs/mozilla-mobile/teams/releng/members)
5. [https://github.com/orgs/mozilla-services/teams/releng/members](https://github.com/orgs/mozilla-services/teams/releng/members)
6. [https://github.com/mozilla-services/cloudops-infra](https://github.com/mozilla-services/cloudops-infra) via filing a ticket [here](https://github.com/mozilla-services/github-management/issues/new?assignees=&labels=&template=NewOrgMember.md&title=) similar to [this](https://github.com/mozilla-services/github-management/issues/129).

There are also a handful of git repos hosted directly by Mozilla. Your manager/mentor will let you know if you need access to one of these.

## Secrets
We have a secrets vault that holds access to various passwords and keys. As you need access to various parts of infra, you will need to get access to the vault. Talk to your manager as this comes up.
Please make sure your SSH and GPG keys are up to date in [https://people.mozilla.org/](https://people.mozilla.org/) to ease the [SOPS](https://github.com/mozilla/sops/) re-encryption. Talk to your manager about this.

In a nutshell, SOPS is a way to track secrets in a Git repository and securely share them with the rest of the team. You'll need to set this up to access credentials and
keys needed for various services Release Engineering uses or administers.

Steps (for MacOSX - but should be similar for Linux, modulo the installation of SOPS):

###### install Google Cloud SDK deps
```
$ curl https://sdk.cloud.google.com | zsh
$ gcloud init
```

###### RelEng currently has two SOPS repositories for holding off secrets.
1. `moz-fx-releng-secrets-global` - this is dedicated for RelEng team secrets (3rd party accounts, certificates, etc).
Basically it's our own private space for holding off any type of secrets. Your manager should be able to grant you access to this repo.
2. `moz-fx-relengworker-prod-a67d` - this is dedicated for our scriptworkers [https://github.com/mozilla-releng/scriptworker-scripts](https://github.com/mozilla-releng/scriptworker-scripts).
It's mirrored to CloudOps infrastructure. This repo is owned by CloudOps, to get access create an issue similar to [SVCSE-242](https://mozilla-hub.atlassian.net/browse/SVCSE-242)

The one that's most commonly used is the global one. The second one is needed only if a new type of scriptworker is added and/or
we're adjusting existing credentials in the release scriptworkers automation.

###### clone the sops repo somewhere on disk
```
$ gcloud source repos clone releng-secrets-global --project=moz-fx-releng-secrets-global
$ gcloud source repos clone secrets-sops-relengworker --project=moz-fx-relengworker-prod-a67d
```
###### install sops
```
$ brew install sops
```

###### acquire new user credentials to talk to the Google Cloud API
```
gcloud auth application-default login
```

###### celebrate by operating the sops credentials
Have a look in the COOKBOOK in the global SOPS repo for more instructions on how to read encrypt/decrypt the files.

:warning: Talk to your manager to add your fingerprint in the SOPS repo and also grant you access in both repos server-side.

###### Disclaimer: Changes ongoing after August 2021
The max session for SOPS credentials has been reset to 24h so there's some commands
that need rerunning in the shell in order to unblock using SOPS.

```
$ gcloud auth login
$ gcloud auth application-default login
```

### Sharing secrets with a co-worker
On a side-note, for sharing secrets between employees, [read these docs](https://mana.mozilla.org/wiki/display/SVCOPS/Sharing+a+secret+with+a+coworker).

## Communication

### Mail
Mozilla mail is handled by Gmail now.

#### Mailing lists

* You should be added to the [release@mozilla.com](release@mozilla.com) google group as a new hire. This mailing list is managed by Google groups. Owners of this group will be able to add you. Send a test message to release@m.c to verify that your address has been added/subscribed. Talk to your manager if it is not working.
* You should be added to the [releng@mozilla.com](releng@mozilla.com) google group as a new hire. This mailing list is managed by Google groups. Owners of this group will be able to add you. Send a test message to releng@m.c to verify that your address has been added/subscribed. Talk to your manager if it is not working.

:warning: release@m.c can contain security-sensitive information. Do not automatically forward your email to a system that is not under Mozilla's control. Same goes for releng@mozilla.com.

#### Mail filtering

With all that new email, you will want to set up some filters in Gmail to handle the higher-volume automated mail.
You may eventually want to take a look at this information, but on day one hundreds of automation notifications are not going to be educational.

:warning: To mitigate the incoming barrage of automated emails download our imperfect, but useful, set of already existing filters.

1. Download [mailFilters.xml](https://raw.githubusercontent.com/mozilla/build-relengdocs/main/procedures/mailFilters.xml)
2. Open [Gmail](https://sso.mozilla.com/gmail)
3. At the top right, click *Settings* and then *See all settings*
4. Click *Filters and Blocked Addresses*
5. At the bottom of the page, click *Import filters*
6. Choose the [mailFilters.xml](https://raw.githubusercontent.com/mozilla/build-relengdocs/main/procedures/mailFilters.xml) file
7. Click *Open file*
8. Click *Create filters*

### Calendar

Like mail, we now use [Google calendar](https://www.google.com/calendar/)

You'll want to subscribe to the following public calendars:
* [RelEng MoCo calendar](https://calendar.google.com/calendar/u/0?cid=bW96aWxsYS5jb21fMmQzMjM0MzMzMzM1MzAzNjMxMmQzOTM3MzdAcmVzb3VyY2UuY2FsZW5kYXIuZ29vZ2xlLmNvbQ)
* [RelEng PTO calendar](https://calendar.google.com/calendar/u/0?cid=Y190cWEzaHQ5bXB0ODN1djJzZDJsYjVsaTVva0Bncm91cC5jYWxlbmRhci5nb29nbGUuY29t)
* [Releases Scheduling](https://calendar.google.com/calendar/embed?src=mozilla.com_dbq84anr9i8tcnmhabatstv5co%40group.calendar.google.com&ctz=Europe%2FLondon)

Talk to your manager/mentor to get added to the various other private calendars as appropriate.

### Matrix

The majority of day-to-day communication in releng happens on Matrix. More details on this can be found on [wiki Matrix](https://wiki.mozilla.org/Matrix).
Please talk to your manager about the private/public channels you should be in.

### Slack

Some parts of Mozilla prefer Slack to Matrix, more info on [mana](https://mana.mozilla.org/wiki/display/SD/Slack).

### Zoom

For video communication we use Zoom. More details can be found on [mana](https://mana.mozilla.org/wiki/display/AVSE/Getting+Started+With+Zoom).

### Wiki

Historical pieces of Mozilla information can be found in wiki.
Request an account filling out [this form](https://wiki.mozilla.org/Special:RequestAccount). You should receive an email with a password in 1-2 days. If not, [file a bug in bugzilla](https://bugzilla.mozilla.org/enter_bug.cgi?product=Websites&component=wiki.mozilla.org).

### Docs

Our single-source of docs is [this](https://docs.mozilla-releng.net/en/latest/). Don't be shy about making improvements to releng pages based on your experiences. Getting someone in releng to review your changes first is good practice. Just ask your team for more details.

### Google Drive

Google Drive (formerly Google docs) is a preferred way to share things these days. This includes spreadsheets and documents that will change a great deal over time.
Google Drive access should be enabled with your email account when you start. If you need access to a particular document, talk to the document owner or your manager/mentor.

## Mana

Some internal Mozilla systems (IT, HR) are documented on [mana](https://mana.mozilla.org/). That is behind SSO and you will be granted access to that as soon as LDAP is activated.

## Future access as you need it
* You will need acccess to our GCP infrastructure. Talk to your manage to be added to the [team-releng@firefox.gcp.mozilla.com](team-releng@firefox.gcp.mozilla.com). Use a ticket similar to [this](https://mozilla-hub.atlassian.net/browse/SVCSE-136) in CloudOps.
* Ship-it - follow procedure in [here](https://moz-releng-docs.readthedocs.io/en/latest/procedures/release-duty/index.html#how-to-get-ship-it-access) to get access.
* Balrog - follow procedure in [here](https://moz-releng-docs.readthedocs.io/en/latest/procedures/release-duty/index.html#how-to-get-balrog-access) to get access. A similar related bug was [bug 1727341](https://bugzilla.mozilla.org/show_bug.cgi?id=1727341).
* CultureAmp - talk to your manager to set your goals and run the logistics in there for the 1x1 tracking. You'll also need to be added to the RelEng team goals.
* JIRA - access to JIRA is granted upon SSO access so please make sure to login via the main dashboard. Ask your manager to add you to the RELENG/FFXP boards.
* Sentry logs - File a bug similar to [this one](https://bugzilla.mozilla.org/show_bug.cgi?id=1731311) to get access to debug various logs in Balrog and more.
* CloudOps Jenkins - File a bug similar to [Bug 1721444](https://bugzilla.mozilla.org/show_bug.cgi?id=1721444) and talk to your manager to get access to Janekins CloudOps to be able to debug. You should already have access to [cloudops-infra repo](https://github.com/mozilla-services/cloudops-infra/) if you've done the Github section above.
Once it's properly configured, you'll be able to access it by making some tweaks documented [here](https://github.com/mozilla-services/cloudops-deployment#accessing-jenkins).

### LDAP groups
* RelEng LDAP flags to access various infrastructure pieces. File a bug similar to [this](https://bugzilla.mozilla.org/show_bug.cgi?id=1732846) and ask your manager for vouching. The flags needed are listed below:

```
cn=active_scm_firefoxci,ou=groups,dc=mozilla
cn=all_scm_firefoxci,ou=groups,dc=mozilla
cn=releng,ou=groups,dc=mozilla
cn=RelEngWiki,ou=groups,dc=mozilla
cn=balrog,ou=groups,dc=mozilla
cn=inventory,ou=groups,dc=mozilla
cn=inventory_build,ou=groups,dc=mozilla
cn=vpn_balrog,ou=groups,dc=mozilla
cn=vpn_cloudops_shipit,ou=groups,dc=mozilla
cn=vpn_releng,ou=groups,dc=mozilla
cn=tooltooleditor,ou=groups,dc=mozilla
cn=scm_firefoxci,ou=groups,dc=mozilla
cn=vpn_releng_loan,ou=groups,dc=mozilla
```
You can view your LDAP groups by accessing the [SSO info page](https://sso.mozilla.com/info)
### Jumphosts

To access any of Release Engineering, Taskcluster, and Release Operations hosts directly, you will need to go through VPN -> Separate MFA -> your target host.
To do that, you and your manager will need to file a ticket against Release Operations and have them send you an invite to add an MFA account on your Duo App.

Example ssh config (adjust the `TODO` to match your own configs)
```
# Ensure KnownHosts are unreadable if leaked - it is otherwise easier to know which hosts your keys have access to.
HashKnownHosts yes
# Host keys the client accepts - order here is honored by OpenSSH
HostKeyAlgorithms ssh-ed25519-cert-v01@openssh.com,ssh-rsa-cert-v01@openssh.com,ssh-ed25519,ssh-rsa,ecdsa-sha2-nistp256-cert-v01@openssh.com,ecdsa-sha2-nistp521-cert-v01@openssh.com,ecdsa-sha2-nistp384-cert-v01@openssh.com,ecdsa-sha2-nistp521,ecdsa-sha2-nistp384,ecdsa-sha2-nistp256

Host hg.mozilla.org git.mozilla.org
    User TODO_USERNAME@mozilla.com
    Compression yes
    ServerAliveInterval 300

Host *.mozilla.com
    User TODO_USERNAME
    IdentityFile ~/.ssh/id_rsa_<TODO_name_of_ssh_private_key>
    Compression yes
    ServerAliveInterval 300

Host *.build.mozilla.org
    Compression yes
    User cltbld
    ServerAliveInterval 300
```


## Good first touchpoint

Following Releaseduty docs to better understand the release mechanics - [https://moz-releng-docs.readthedocs.io/en/latest/procedures/release-duty/index.html](https://moz-releng-docs.readthedocs.io/en/latest/procedures/release-duty/index.html)
