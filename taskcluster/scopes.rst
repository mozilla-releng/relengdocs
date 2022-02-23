.. _scopes:

Scopes
======

Scopes are effectively permissioning, or ACLs, for Taskcluster. The official definition of scopes is `here <https://firefox-ci-tc.services.mozilla.com/docs/manual/access-control/api#scopes-and-roles>`__. They're essentially strings; if your set of scopes or scope patterns match the required scopes, you have the required scopes.

For example, if you have the scopes::

    queue:get-artifact:releng/super-sekrit/*
    queue:get-artifact:releng/a-little-bit-secret/something

And the required scopes are::

    queue:get-artifact:releng/super-sekrit/one
    queue:get-artifact:releng/a-little-bit-secret/something

Then you have the required scopes. However, if you need ``a-little-bit-secret/something-else``, you don't have the required scopes.

Ci-configuration
----------------

We grant scopes to clients and roles. These are defined in the `ci-configuration repo <https://hg.mozilla.org/ci/ci-configuration/>`__; view the `README <https://hg.mozilla.org/ci/ci-configuration/file/tip/README.md>`__.

The ci-configuration repo also contains the `ci-admin` management tool which we use to test, diff, and apply the configuration changes.

Conventions
-----------

Delimiters
~~~~~~~~~~

Colons ``:`` are delimiters for the official platform defined scopes and scope prefixes. We also use dashes ``-`` and slashes ``/`` as word delimiters in the user-defined portions of the scope strings. (Also, periods ``.`` for index delimiters.) If you define a scope pattern with a trailing asterisk ``*``, it's best practice to append the asterisk after a word delimiter::

    queue:get-artifact:releng/super-sekrit/*

rather than::

    queue:get-artifact:releng/super-sekrit*

Groups / teams
~~~~~~~~~~~~~~
We try to tie most user scope grants to LDAP. Grants to ``mozilla-group:GROUP`` will assign the scopes to users that belong to that MoCo ldap group. Grants to ``mozillians-group:GROUP`` will grant scopes to users that belong to that Mozillians group (`people.mozilla.org <https://people.mozilla.org>`__).

We also define ``ci-group`` roles like ``project:releng:ci-group:team_moco`` in `this block <https://hg.mozilla.org/ci/ci-configuration/file/307d8717f17e3916ebdfc54e58705230c5cf30a7/grants.yml#l2351>`__.

Levels
~~~~~~

Levels in scopes match the Firefox commit levels. Level 1 is Try and pull requests; contributors can easily get this level of access. Level 2 is projects and l10n, and isn't used everywhere. Level 3 is release level, and requires a higher bar to gain this level of access. Ideally contributors will be able to get everything done at level 1 unless they become a trusted member of a project.

We encode levels in workerType/workerPool names, and in other scopes that should be restricted by repo and commit level. For example, the ``gecko-1/decision`` worker is the decision worker for Try. ``gecko-3/decision`` is the trusted decision worker for release trains and autoland.

Docker- and Generic-Worker scopes
---------------------------------

The scopes for docker- and generic-worker workers should be minimal, just enough to register as a given workerType and claim tasks from the queue. They will be granted temporary scopes for each task that they run.

Scriptworker scopes
-------------------

Scriptworker scopes are similar, but each ``*script`` will also define script-specific scopes, like ``project:releng:signing:format:signcode``.

In addition, until we fix `Issue #426 (use temp queue to download artifacts) <https://github.com/mozilla-releng/scriptworker/issues/426>`__, we also need to grant private artifact scopes to the *clientId* as well as the task.

Restricted scopes
~~~~~~~~~~~~~~~~~

We define Chain of Trust `cot_restricted_scopes <https://github.com/mozilla-releng/scriptworker/blob/dd0eed21354ecfabbe5838ea3cf730ff0630a3dd/src/scriptworker/constants.py#L361-L445>`__ in scriptworker. These are scopes that can only run on specific allowlisted trees or ``tasks_for``.
