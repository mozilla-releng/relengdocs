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
which require that status need to be check and revoked. (Refer to the
`day one`_ page for details on permissions.) Legend:

|   RE:  Release Engineering team member
|   Emp: Mozilla Corporation employee
|   CM:  Contributing community Member


.. _`day one`: https://wiki.mozilla.org/ReleaseEngineering/Day_1_Checklist

    +----+-----+----+------------------------------------------------------------------------------------------------------------------------+
    | RE | Emp | CM | Permission                                                                                                             |
    +====+=====+====+========================================================================================================================+
    | X  |     |    | access to releng secrets [#secrets]_                                                                                   |
    +----+-----+----+------------------------------------------------------------------------------------------------------------------------+
    | X  |     |    | balrog [#special]_                                                                                                     |
    +----+-----+----+------------------------------------------------------------------------------------------------------------------------+
    | X  | X   |    | releng LDAP bits (IT bug) releng, vpn_releng, RelengWiki, & SysAdminWiki                                               |
    +----+-----+----+------------------------------------------------------------------------------------------------------------------------+
    | X  |     |    | mac signers acces                                                                                                      |
    +----+-----+----+------------------------------------------------------------------------------------------------------------------------+
    | :ref:`miscellaneous systems<misc_systems>`                                                                                             |
    +----+-----+----+------------------------------------------------------------------------------------------------------------------------+
    | X  | X   |    | github ownership roles [#github]_                                                                                      |
    +----+-----+----+------------------------------------------------------------------------------------------------------------------------+
    | X  |     |    | hg.mozilla.org special access [#hgmo]_                                                                                 |
    +----+-----+----+------------------------------------------------------------------------------------------------------------------------+
    | X  | X   |    | github write access (review)                                                                                           |
    +----+-----+----+------------------------------------------------------------------------------------------------------------------------+
    | X  |     |    | releng/build bugzilla group access [#bugzilla]_                                                                        |
    +----+-----+----+------------------------------------------------------------------------------------------------------------------------+
    | X  | X   |    | Google Drive RelEng folder access                                                                                      |
    +----+-----+----+------------------------------------------------------------------------------------------------------------------------+
    | X  | X   |    | Release google calendar                                                                                                |
    +----+-----+----+------------------------------------------------------------------------------------------------------------------------+
    | X  | X   |    | Release google group                                                                                                   |
    +----+-----+----+------------------------------------------------------------------------------------------------------------------------+
    | X  |     |    | re-assign bugs                                                                                                         |
    +----+-----+----+------------------------------------------------------------------------------------------------------------------------+

Password List
^^^^^^^^^^^^^

.. [#secrets]

    RelEng passwords and other credentials are stored in a `SOPS <https://github.com/mozilla/sops>` repository.

.. [#special]

    Balrog: Add ACLs on `the admin UI <https://balrog.services.mozilla.com/users>`


.. _misc_systems:

Miscellaneous Systems
^^^^^^^^^^^^^^^^^^^^^

These systems are unique, so you may need to refer to other
documentation for instructions.

.. [#hgmo]

    There are some hand maintained white lists for push permissions to
    certain branches. (E.g. puppet production) Changes need to be
    approved by a RelEng/RelOps manager.

.. [#github]

    For now, the accounts to check are `mozilla` & `mozilla-releng`, `mozilla-mobile`, `mozilla-extensions`, and `mozilla-partners`.  Note
    that we're only discussing the ownership role here on RelEng owned
    resources. If the person has ownership rights to repositories due to
    their contributor status, that does not change.

.. [#bugzilla]

    This bugzilla group can cause some confusion for folks transitioning
    out of MoCo but remaining a RelEng contributor.  Perform on the
    `admin
    <https://bugzilla.mozilla.org/editusers.cgi?action=list&matchvalue=login_name&matchstr=&matchtype=substr&grouprestrict=1&groupid=34>`_
    page.


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
