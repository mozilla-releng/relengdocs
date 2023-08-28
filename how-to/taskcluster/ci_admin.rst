.. _ci-admin:

CI-Admin
========

This page contains some information about the ci-admin tool, and how to use it.

Through cloudops-jenkins
------------------------

This is the best practice way to apply changes: we know we're running the check before we apply; we don't use root perms locally; we know we're running against the tip of the official repo.

Once we land a change in `ci-configuration`_, cloudops-jenkins picks up that change through Pulse, and we run `this command <https://github.com/mozilla-services/cloudops-infra/blob/71f6992da04384f252c0e67ae55c527bd34ede85/projects/taskcluster/tasks#L114-L164>`__. After we landed `this fix <https://github.com/taskcluster/tc-admin/pull/195>`__ this has been fairly quick.

We currently run against the ``staging`` cluster first, then the ``firefoxci`` cluster, but staging failures don't block the production run.

Known Issues
~~~~~~~~~~~~

Twice in the past ~month (as of 2022.01.20), we've had issues with `pulse-go <https://github.com/taskcluster/pulse-go/issues/7>`__ dropping the Pulse connection and requiring a manual kick.

Manually
--------

Sometimes you want to run ci-admin manually. Generally this is when cloudops-jenkins isn't responding and we have an urgent bustage fix.


Setup
~~~~~

1. Clone `ci-configuration`_.

.. ATTENTION::
   Make sure your local checkout of ci-configuration is clean, and at the tip revision!

Otherwise you can apply an old or wip revision to the production cluster config.

You can do this via::

    hg status
    hg checkout -r 'last(public())'  # make sure we're not on a wip revision
    hg pull -u
    hg ident  # verify against latest revision on hgweb

2. Install ci-admin into a virtualenv::

    # activate virtualenv, py>=3.7
    cd ci-configuration
    pip install -r requirements/local.txt
    python setup.py develop

Run
~~~

1. Diff::

    ci-admin diff --environment firefoxci 2>&1 | tee diff.out

If you get a permissions issue here, try logging out of taskcluster::

    unset TASKCLUSTER_CLIENT_ID; unset TASKCLUSTER_ACCESS_TOKEN

If you get a mismatch in root url, set it to prod::

    export TASKCLUSTER_ROOT_URL=https://firefox-ci-tc.services.mozilla.com/

In theory you should only see the changes that have landed since the last run of ci-admin. However, you may see other diffs.

One reason is someone's modified a taskcluster.yml (see :ref:`actions_tc_yml`). Another reason is someone may have modified the running production cluster config, possibly by running ci-admin manually.

2. Check::

    ci-admin check --environment firefoxci 2>&1 | tee check.out

This runs through various tests of the configs. This takes time, and sometimes we skip this if we're confident in the changes and need to roll things out quickly.

3. Apply::

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

.. _ci-configuration: https://hg.mozilla.org/ci/ci-configuration/
