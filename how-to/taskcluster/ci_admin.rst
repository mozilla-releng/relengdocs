.. _ci-admin:

CI-Admin
========

This page contains some information about the ci-admin tool, and how to use it.

Through github actions
----------------------

This is the best practice way to apply changes: we know we're running the check before we apply; we don't use root perms locally; we know we're running against the tip of the official repo.

Once we land a change in `fxci-config`_, a GHA `workflow <https://github.com/mozilla-releng/fxci-config/blob/main/.github/workflows/deploy.yml>`__ is triggered.

We currently run against the ``staging`` cluster and the ``firefoxci`` cluster independently.

Manually
--------

Sometimes you want to run ci-admin manually. Generally this is when we have an urgent bustage fix.

If possible you should avoid running tc-admin locally and re-run the latest `apply (firefoxci)` workflow on the repo's main branch instead.

Setup
~~~~~

1. Clone `fxci-config`_.

.. ATTENTION::
   Make sure your local checkout of fxci-config is clean, and at the tip revision!

Otherwise you can apply an old or wip revision to the production cluster config.

You can do this via::

    git checkout main
    git pull upstream main

2. Install ci-admin into a virtualenv::

    # activate virtualenv, py>=3.7
    cd fxci-config
    pip install -r requirements/local.txt
    python setup.py develop

Run
~~~

1. Diff::

    # Ensure you have a GITHUB_TOKEN in your environment to avoid rate limiting
    # when ci-admin queries github.com repositories.
    export GITHUB_TOKEN=xxxxxxxxxx

    # Setup Taskcluster credentials that have enough scopes to run a diff
    eval $(taskcluster signin -s auth:list-clients)

    ci-admin diff --environment firefoxci 2>&1 | tee diff.out

If you get a mismatch in root url, set it to prod::

    export TASKCLUSTER_ROOT_URL=https://firefox-ci-tc.services.mozilla.com/

In theory you should only see the changes that have landed since the last run of ci-admin. However, you may see other diffs.

One reason is someone's modified a taskcluster.yml (see :ref:`actions_tc_yml`). Another reason is someone may have modified the running production cluster config, possibly by running ci-admin manually.

2. Check::

    ci-admin check --environment firefoxci 2>&1 | tee check.out

This runs through various tests of the configs. This takes time, and sometimes we skip this if we're confident in the changes and need to roll things out quickly.

3. Apply::

    # Ensure you have a GITHUB_TOKEN in your environment to avoid rate limiting
    # when ci-admin queries github.com repositories.
    export GITHUB_TOKEN=xxxxxxxxxx

    # Setup Taskcluster credentials that have enough scopes to run a diff
    eval $(taskcluster signin --expires 15m)

    ci-admin apply --environment firefoxci 2>&1 | tee apply.out

You may want to log out explicitly after this to avoid hitting errors with expired creds::

    unset TASKCLUSTER_CLIENT_ID; unset TASKCLUSTER_ACCESS_TOKEN

Applying local changes
^^^^^^^^^^^^^^^^^^^^^^

.. Attention::
   This goes even further against best practices.
   Only do this if there is a compelling reason to.

First, whatever is in your local clone gets applied, so you can patch the config before running ``ci-admin``.

Second, you can use the ``--grep`` option to various ``ci-admin`` commands, namely ``diff`` and ``apply``, to only apply the changes that match the ``--grep`` string. This allows you to, say, apply scopes changes to a staging repo, without blowing away someone else's testing changes in, say, a worker pool.

.. Attention::
   Your local changes will be blown away the next full ci-admin run!

.. _fxci-config: https://github.com/mozilla-releng/fxci-config
