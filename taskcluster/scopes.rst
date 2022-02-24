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

Roles
-----

`Roles <https://firefox-ci-tc.services.mozilla.com/auth/roles>`__ are a way of grouping sets of scopes together. If you're granted the ``assume:<role>`` scope, you are granted each of the scopes in that role. (See `Scopes and Roles <https://docs.taskcluster.net/docs/manual/access-control/api#scopes-and-roles>`__.)

Expansion of scopes in Automation
---------------------------------

It's not intuitive at first which scopes are granted and which are required in automation. This is at least partially because scopes are expanded from a simple single role to a massive set. Star scopes expand to match any number of matching scopes, and each one of those allow for further expansion.

(There's a handy `tool <https://firefox-ci-tc.services.mozilla.com/auth/scopes/expansions?scopes%5B0%5D=assume%3Arepo%3Ahg.mozilla.org%2Fmozilla-central%3Abranch%3Adefault>`__ that lets us put in a scope or scopes, then click the ``expand scopes`` button in the lower right, to list the full set of scopes granted.)

Hg Pushes
~~~~~~~~~

For hg.m.o, pushes go through hooks. (see :ref:`how_tasks_are_triggered`.) By default we'll assume the role e.g. ``hook-id:hg-push/mozilla-central`` in this hook. The ``create-task`` scopes limit what worker pools we can create tasks for, and we can only grant scopes to tasks within the set of scopes that the hook has been granted. (If the hook has scopes ``["foo", "bar"]``, it can schedule tasks with the scopes ``["foo"]``, ``["bar"]``, or ``["foo", "bar"]`` but not ``["foo", "baz"]``.)

The `hg-push template <https://hg.mozilla.org/ci/ci-configuration/file/ef4fae54de4063ab072aa6c203d72de036817641/hg-push-template.yml>`__ grants the scope ``assume:${project_role_prefix}:branch:*``, e.g. `assume:repo:hg.mozilla.org/mozilla-central:branch:* <https://firefox-ci-tc.services.mozilla.com/auth/scopes/expansions?scopes%5B0%5D=assume%3Arepo%3Ahg.mozilla.org%2Fmozilla-central%3Abranch%3A%2A>`__ to the build-decision task, which means the decision task can have a subset of those scopes.

The decision task itself will have the scopes defined in `.taskcluster.yml <https://hg.mozilla.org/mozilla-central/file/fb443d9a5f9cfaa17acc81c25473d7093d5cf696/.taskcluster.yml#l154>`__, which will be a subset of the build-decision task's scopes (or we'll fail due to insufficient scopes).

TC-Github
~~~~~~~~~

Taskcluster-github grants `these scopes <https://github.com/taskcluster/taskcluster/blob/1226549dec4e543579192787ae56101fd85d7203/services/github/src/tc-yaml.js#L40-L58>`__ to tasks depending on their Github event type.

Cron
~~~~

Similar to hg pushes, cron goes through hooks (see :ref:`how_tasks_are_triggered`). By default we'll assume the role e.g. ``hook-id:project-releng/cron-task-mozilla-central`` in this hook.

The `cron task template <https://hg.mozilla.org/ci/ci-configuration/file/ef4fae54de4063ab072aa6c203d72de036817641/cron-task-template.yml>`__ grants the scope ``assume:hook-id:${hookGroupId}/${hookId}``, so the resulting build-decision task will have the same set of scopes as the hook.

The cron task itself will have the scopes defined in `.taskcluster.yml <https://hg.mozilla.org/mozilla-central/file/fb443d9a5f9cfaa17acc81c25473d7093d5cf696/.taskcluster.yml#l154>`__, which will be a subset of the build-decision task's scopes (or we'll fail due to insufficient scopes).

Actions
~~~~~~~

Actions check for a special scope, `assume:repo:{head_repository[8:]}:action:{actionPerm} <https://hg.mozilla.org/ci/taskgraph/file/1d87180150c4831cba1cc7c871cac75a6463643e/src/taskgraph/actions/registry.py#l307>`__. ``actionPerm`` falls back to ``generic`` for many actions, which means they're all permissioned the same. An action like `retrigger-decision <https://hg.mozilla.org/ci/taskgraph/file/1d87180150c4831cba1cc7c871cac75a6463643e/src/taskgraph/actions/retrigger.py#l43>`__ or `release-promotion <https://github.com/mozilla-mobile/fenix/blob/c4c263abcba81c689dc22e0d666d1979f0733aeb/taskcluster/fenix_taskgraph/release_promotion.py#L28-L33>`__ will not specify ``generic=True``, and their ``actionPerm`` will be ``retrigger-decision`` or ``release-promotion``, respectively; this lets us grant these scopes more selectively.

Misc
~~~~

We're able to target our scope grants fairly granularly. For example, `this block <https://hg.mozilla.org/ci/ci-configuration/file/ef4fae54de4063ab072aa6c203d72de036817641/grants.yml#l474>`__::

    - grant:
      - project:releng:balrog:server:beta
      - project:releng:balrog:server:esr
      - project:releng:balrog:server:release
      - project:releng:beetmover:bucket:maven-production
      - project:releng:beetmover:bucket:partner
      - project:releng:beetmover:bucket:release
      - project:releng:bouncer:server:production
      - project:releng:bouncer:server:production-nazgul
      - project:releng:ship-it:server:production
      to:
      - projects:
          job: ["action:release-promotion"]
          trust_domain: gecko
          level: [3]
          alias: [mozilla-esr78, mozilla-esr91, mozilla-release, mozilla-beta]

lets us grant restricted scriptworker scopes to just the release promotion action, run on level 3 gecko repositories, as long as their aliases match one of the above. Phew! Where we run into issues is if we, say, want to run a retrigger action hook on one of those tasks. Because the retrigger action hook doesn't match the above filter, it won't have the scopes to create the retriggered task. (Perhaps this is all for the best, given :ref:`the issues with retriggering release tasks <deadline_exceeded_release_task_retrigger>`.

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
