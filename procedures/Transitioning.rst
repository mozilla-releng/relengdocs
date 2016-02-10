.. Releng Permissions documentation master file, created by
   sphinx-quickstart on Sun Aug 24 11:56:58 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===========================
Transitioning RelEng Status
===========================

Overview
========

From time to time, folks move in and out of the Release Engineering
role. As they do so, access to various systems should be granted and
removed [*]_ .

When someone moves into the organization, permissions should be granted
as needed to perform the various tasks. While permissions are granted
only as needed, there are also minimum requirements for the permissions.
For example, some permissions may only be available to someone who is
both a member of the RelEng team and an employee.

The table below lists all the permissions, and which requirements are required
to have that permission. When a person no longer has a specific status, all permissions
which require that status need to be check and revoked. Legend:

|   RE:  Release Engineering team member
|   Emp: Mozilla Corporation employee
|   CM:  Contributing community Member

    +----+-----+----+------------------------------------------------------+
    | RE | Emp | CM | Permission                                           |
    +====+=====+====+======================================================+
    |                     :ref:`password changes:<password_list>`          |
    +----+-----+----+------------------------------------------------------+
    | X  |     |    | access to releng password files [#passwords]_        |
    +----+-----+----+------------------------------------------------------+
    | X  | X   |    | #mozbuild password [#mozbuild]_                      |
    +----+-----+----+------------------------------------------------------+
    | X  |     |    | bouncer [#special]_                                  |
    +----+-----+----+------------------------------------------------------+
    | X  |     |    | balrog [#special]_                                   |
    +----+-----+----+------------------------------------------------------+
    | X  |     |    | treestatus [#special]_                               |
    +----+-----+----+------------------------------------------------------+
    | X  |     |    | releng etherpad account [#special]_                  |
    +----+-----+----+------------------------------------------------------+
    | X  |     |    | cltbld & root slave farm password                    |
    +----+-----+----+------------------------------------------------------+
    | X  |     |    | releng puppet masters                                |
    +----+-----+----+------------------------------------------------------+
    |                    :ref:`compute resources<compute_resources>`       |
    +----+-----+----+------------------------------------------------------+
    | X  | X   | X  | AWS console access                                   |
    +----+-----+----+------------------------------------------------------+
    | X  | X   |    | releng LDAP bits (IT bug) releng & vpn_releng        |
    +----+-----+----+------------------------------------------------------+
    | X  |     |    | unassign any resources in slavealloc                 |
    +----+-----+----+------------------------------------------------------+
    | X  |     |    | RelEng machine access e.g. cruncher,                 |
    |    |     |    | stage, buildbot masters, etc. [#ssh_login]_          |
    +----+-----+----+------------------------------------------------------+
    |                    :ref:`miscellaneous systems<misc_systems>`        |
    +----+-----+----+------------------------------------------------------+
    | X  | X   |    | github ownership roles [#github]_                    |
    +----+-----+----+------------------------------------------------------+
    |    |     | X  | github write access                                  |
    +----+-----+----+------------------------------------------------------+
    | X  |     |    | releng/build bugzilla group access [#bugzilla]_      |
    +----+-----+----+------------------------------------------------------+
    | X  | X   |    | Google Drive RelEng folder access                    |
    +----+-----+----+------------------------------------------------------+
    | X  | X   |    | Release google group                                 |
    +----+-----+----+------------------------------------------------------+
    | X  |     |    | other Google Drive documents [#gd_docs]_             |
    +----+-----+----+------------------------------------------------------+
    | X  |     |    | re-assign bugs                                       |
    +----+-----+----+------------------------------------------------------+
    | X  |     |    | named contact in Nagios escalation chain             |
    +----+-----+----+------------------------------------------------------+
    | X  |     |    | Allowed to merge to puppet production [#special]_    |
    +----+-----+----+------------------------------------------------------+

Detailed Instructions
---------------------
.. _password_list:

Password List
^^^^^^^^^^^^^

.. [#passwords]

    Almost all passwords are now shared via gpg encrypted files. To get a
    list of passwords shared with a user, use `this script
    <https://hg.mozilla.org/build/braindump/file/default/utils/list-gpg-recipients>`_
    to identify the passwords which need to be changed. Also, add the
    departing user's id to the `alumni.json
    <http://hg.mozilla.org/build/braindump/file/default/utils/alumni.json>`_
    file.

.. [#mozbuild]

    To change the password on an IRC channel where you have ops
    permissions:
        
        - Make sure user is *not* in #mozbuild, a kick or ban is
          sometimes necessary (due to auto-reconnect)
        - ``/msg chanserv set #mozbuild mlock +k newpass``

.. [#special]

    Bouncer: change via `bounceradmin.m.c <https://bounceradmin.mozilla.com/admin/auth/user/>`_

    Balrog: go to permissions from `<https://aus4-admin.mozilla.org/rules.html>`_

    Treestatus: from `users <https://treestatus.mozilla.org/users>`_
    page.

    Puppet Merge: commit update to `hook
    <https://hg.mozilla.org/hgcustom/version-control-tools>` and request
    deploy.

        
.. _compute_resources:

Compute Resources
^^^^^^^^^^^^^^^^^

In addition to password changes governing access to compute resources, a
scan of systems must be made to ensure no processes or cron jobs have
been left running.

.. [#ssh_login]

    These are systems where the user is granted access via their ssh
    key, either to their user specific account, or to a shared account
    (such as ``cltbld``). However, these systems have keys deployed via
    the RelEng puppet servers, which do not auto-sync with MoCo ldap
    systems. A bug needs to be opened with RelOps to sync the ldap data
    in order to propegate any status change.

.. _misc_systems:

Miscellaneous Systems
^^^^^^^^^^^^^^^^^^^^^

These systems are unique, so you may need to refer to other
documentation for instructions.

.. [#github]

    For now, the accounts to check are `mozilla` & `mozilla-b2g`.  Note
    that we're only discussing the ownership role here on RelEng owned
    resources. If the person has ownership rights to repositories due to
    their contributor status, that does not change.

.. [#bugzilla]

    This bugzilla group can cause some confusion for folks transitioning
    out of MoCo but remaining a RelEng contributor.  Perform on the
    `admin
    <https://bugzilla.mozilla.org/editusers.cgi?action=list&matchvalue=login_name&matchstr=&matchtype=substr&grouprestrict=1&groupid=34>`_
    page.

.. [#gd_docs]

  To find documents where exceptional access has been granted, use the
  script at http://labnol.org/?p=28237


Footnotes
---------

.. [*]

    Unlike most of Mozilla development, some Release Engineering roles
    are only available to employees for various legal or contractual
    reasons. That leads to layers of access:

        RelEng:
            Folks directly performing tasks which require knowledge of
            how Release Engineering systems work and interact.

        MoCo Emp:
            Folks who have a contractual arrangement with Mozilla that
            may be required for access to certain restricted systems and
            data.

        Contributors:
            Folks who have valid committer's agreement on file.

