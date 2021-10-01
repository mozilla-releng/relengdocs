# Taskcluster command line interface (CLI)

The Taskcluster Command Line Interface (CLI) source and docs are [here](https://github.com/taskcluster/taskcluster/tree/main/clients/client-shell). Prebuilt Linux and Mac Taskcluster CLI binaries are available [here](https://github.com/taskcluster/taskcluster/releases).

## Difference between actions and CLI

Taskcluster action hooks, as implemented in taskgraph, are one way to perform similar tasks as the CLI, especially in regard to cancelling, rerunning, or retriggering tasks.

They differ in a few ways:

1. You need a different set of scopes to trigger action hooks than to cancel, rerun, or retrigger tasks directly. For action hooks, you might need a scope like `hooks:trigger-hook:project-gecko/in-tree-action-1-generic/*` . For the CLI, you might need a scope like `queue:rerun-task:gecko-level-1/*`

2. Actions use the logic supplied in `taskgraph`. The CLI hits the Taskcluster API directly. Oftentimes this can result in similar behavior. But, for example, Github PRs from a non-privileged fork might not allow for rerunning, retriggering, or cancelling tasks through action hooks, while someone with scopes may be able to via the CLI.

   (A related point: permissions are more granular for action hooks; the CLI may allow for more broad access.)

3. Tasks generated through action hooks can be verifiable by the Chain of Trust (CoT). Tasks generated through, e.g., `taskcluster task retrigger -- TASKID` are not. (This CLI call creates a new task without an action or decision task, which prevents CoT from verifying.)

   (Since a `taskcluster task rerun -- TASKID` doesn't **generate** a new task but merely increments the `runId`, that task should remain CoT-verifiable if it was CoT-verifiable originally.)

## Taskcluster CLI best practices

### Principle of Least Privilege

We should follow the [principle of least privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege). Although Releng has effective root on the FirefoxCI cluster, let's not perform everyday actions using root privileges. Setting short expiries and the minimal amount of scopes needed to perform a given task helps avoid a) leaking scopes that can cause a lot of damage, and/or b) accidentally running the wrong command in a shell and doing damage to the production cluster.

### Aliases

By setting aliases in our shells, we can perform common tasks without having to memorize the syntax every time. Here are a few aliases that may be helpful:

```
# To set your root URL to the production firefoxci or stage cluster
tc-fxci='export TASKCLUSTER_ROOT_URL=https://firefox-ci-tc.services.mozilla.com/'
tc-staging='export TASKCLUSTER_ROOT_URL=https://stage.taskcluster.nonprod.cloudops.mozgcp.net/'

# To log out explicitly
tc-logout='unset TASKCLUSTER_CLIENT_ID; unset TASKCLUSTER_ACCESS_TOKEN'

# Rerunning and cancelling tasks are a common request/need in releaseduty;
# grant this set of scopes for 1 hour
tc-relduty=$'eval `TASKCLUSTER_ROOT_URL=https://firefox-ci-tc.services.mozilla.com/ taskcluster signin --expires 1h -s "queue:rerun-task:*\nqueue:cancel-task:*"`'

# Up to root privs: only grant these for 15min
tc-signin='eval `TASKCLUSTER_ROOT_URL=https://firefox-ci-tc.services.mozilla.com/ taskcluster signin --expires 15m "$@"`'
```
