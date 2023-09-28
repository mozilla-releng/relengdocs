.. _taskcluster_cli:

Taskcluster command line interface (CLI)
========================================

The Taskcluster Command Line Interface (CLI) source and docs are
`here <https://github.com/taskcluster/taskcluster/tree/main/clients/client-shell>`__.
Prebuilt Linux and Mac Taskcluster CLI binaries are available
`here <https://github.com/taskcluster/taskcluster/releases>`__.

Difference between actions and CLI
----------------------------------

Taskcluster action hooks, as implemented in taskgraph, are one way to
perform similar tasks as the CLI, especially in regard to cancelling,
rerunning, or retriggering tasks.

They differ in a few ways:

1. You need a different set of scopes to trigger action hooks than to
   cancel, rerun, or retrigger tasks directly. For action hooks, you
   might need a scope like
   ``hooks:trigger-hook:project-gecko/in-tree-action-1-generic/*`` . For
   the CLI, you might need a scope like
   ``queue:rerun-task:gecko-level-1/*``

2. Actions use the logic supplied in ``taskgraph``. The CLI hits the
   Taskcluster API directly. Oftentimes this can result in similar
   behavior. But, for example, Github PRs from a non-privileged fork
   might not allow for rerunning, retriggering, or cancelling tasks
   through action hooks, while someone with scopes may be able to via
   the CLI.

   (A related point: permissions are more granular for action hooks; the
   CLI may allow for more broad access.)

3. Tasks generated through action hooks can be verifiable by the Chain
   of Trust (CoT). Tasks generated through, e.g.,
   ``taskcluster task retrigger -- TASKID`` are not. (This CLI call
   creates a new task without an action or decision task, which prevents
   CoT from verifying.)

   (Since a ``taskcluster task rerun -- TASKID`` doesn’t **generate** a
   new task but merely increments the ``runId``, that task should remain
   CoT-verifiable if it was CoT-verifiable originally.)

Taskcluster CLI best practices
------------------------------

Principle of Least Privilege
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We should follow the `principle of least
privilege <https://en.wikipedia.org/wiki/Principle_of_least_privilege>`__.
Although Releng has effective root on the FirefoxCI cluster, let’s not
perform everyday actions using root privileges. Setting short expiries
and the minimal amount of scopes needed to perform a given task helps
avoid a) leaking scopes that can cause a lot of damage, and/or b)
accidentally running the wrong command in a shell and doing damage to
the production cluster.

Signin Helper
~~~~~~~~~~~~~

Using this shell helper function is an easy way to ensure only the minimum
amount of scopes are being used:

.. code-block:: shell

   tc-signin () {
       if [[ "$#" == "0" ]]; then
           echo "error: must provide use case"
           return 1
       fi
       purpose="$1"
       shift
   
       case $purpose in
           ciadmin)
               expiry="60m"
               scopes=(
                   "hooks:list-hooks:*"
               )
               ;;
           relduty)
               expiry="60m"
               scopes=(
                   "queue:rerun-task:*"
                   "queue:cancel-task:*"
               )
               ;;
           hook)
               expiry="15m"
               scopes=(
                   "hooks:trigger-hook:*"
               )
               ;;
           root)
               expiry="15m"
               scopes=(
                   "*"
               )
               ;;
           *)
               echo "error: invalid use case '$purpose'"
               return 1
       esac
   
       scope_str=$(IFS=$'\n' ; echo "${scopes[*]}")
       tc_url="${TASKCLUSTER_ROOT_URL:-https://firefox-ci-tc.services.mozilla.com}"
       eval "$(TASKCLUSTER_ROOT_URL=$tc_url taskcluster signin --expires=$expiry --scope="$scope_str")"
   }
   
   tc-signout () {
       unset TASKCLUSTER_CLIENT_ID
       unset TASKCLUSTER_ACCESS_TOKEN
   }

Add this function to your ``~/.bashrc`` or equivalent. Feel free to edit the
function and populate it with the use cases most relevant to your needs. It can
be used like this:

.. code-block:: shell

   $ tc-signin ciadmin
   # run ciadmin commands
   $ tc-signout

Using ``tc-signin root`` should be a method of last resort.
