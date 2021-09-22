# Testing Actions

Actions in Taskgraph allow for adding, cancelling, retriggering/rerunning tasks in/to the graph. The action docs are currently [here](https://firefox-source-docs.mozilla.org/taskcluster/actions.html?highlight=action).

We can test any available action with `[./mach] taskgraph test-action-callback`, which takes input (schemas are defined per action), parameters, and taskId/taskGroupId commandline options. You can run `[./mach] taskgraph test-action-callback --help` for more information.

A successful `[./mach] taskgraph test-action-callback` run will create an `artifacts` directory in the current working directory (or `cwd`), which is the base of the repo. This `artifacts` directory will contain the same artifacts that the action task would have created, had it run in automation. This will generally include information about tasks it would have scheduled, cancelled, reran or retriggered.

(We use `./mach taskgraph test-action-callback` in Gecko, and `taskgraph test-action-callback` in standalone taskgraph projects. The square brackets around `[./mach]` indicate that we may or may not need to include it in the command, depending on which project we're testing.)

As of this writing (2021.09.21) Gecko actions are all defined in the [actions directory](https://searchfox.org/mozilla-central/source/taskcluster/taskgraph/actions) in-Gecko-tree. Standalone taskgraph actions are either defined [in taskgraph](https://hg.mozilla.org/ci/taskgraph/file/tip/src/taskgraph/actions) or in each repo (e.g. [Fenix relpro](https://github.com/mozilla-mobile/fenix/blob/main/taskcluster/fenix_taskgraph/release_promotion.py))

## Testing Release Promotion actions

The Release Promotion action exists in multiple repositories ([Gecko, for example](https://searchfox.org/mozilla-central/source/taskcluster/taskgraph/actions/release_promotion.py), or [Fenix](https://github.com/mozilla-mobile/fenix/blob/main/taskcluster/fenix_taskgraph/release_promotion.py)), and tends to be customized for each product. Each follows similar patterns, however. For instance, each follows the [☃ model](https://docs.google.com/presentation/d/1xCQZfLzCto0faO2AHXIsL-Xr-SsL2NnAVqSGbWGEcrg/edit?usp=sharing). Each consists of various `phases`, e.g. `build`, `promote`, `push`, and `ship` for Gecko releases.

### Replicating an existing release graph

### Example promotion test

### Advanced usage

#### `rebuild_kinds` and `do_not_optimize`

#### Using multiple revisions

#### Using the tested input to craft a custom release graph
