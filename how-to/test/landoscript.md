# Landoscript

This page covers how to test [landoscript](https://github.com/mozilla-releng/scriptworker-scripts/tree/master/landoscript) beyond running unit tests.

In addition to what's here, it's useful to familiarize yourself with more general [scriptworker](https://scriptworker.readthedocs.io/en/latest/index.html) and [scriptworker-scripts](https://scriptworker-scripts.readthedocs.io/en/latest/index.html) documentation.

Overview
--------

The tl;dr of landoscript is that it is responsible for making changes to github repositories that can only be modified by submitting changes to the [Lando API](https://lando.moz.tools/).

All landoscript tasks (as of the time of writing) support a dry run mode, which will execute everything that a non-dry run task will, but bail out just before submitting the changes to Lando (which is the final step of the task). This makes it easy to run fairly extensive integration tests without making changes to any repositories, which gives a fairly high measure of confidence.

There are two ways to run dry runs:
* Running landoscript locally. This is slightly more work to set-up initially, but makes iteration significantly faster. This method is recommended for early development or when less confident in the changes you're making.
* Running landoscript tasks on try. These are much easier to run, but it can take 20 minutes or more per iteration. These can be OK if you have high confidence in your changes, or are OK with the long iteration times.

Additionally, landoscript can be run out of dry run mode on [Try](https://treeherder.mozilla.org/jobs?repo=try), and will make changes to [https://github.com/mozilla-releng/staging-firefox](https://github.com/mozilla-releng/staging-firefox). These tests should usually be done before submitting a patch for review, but because they modify a repository they are sometimes trickier or more involved to set-up, and are often saved for a final sanity check. (More on this below.)

## Testing Locally

This is covered at a high level in [the scriptworker-scripts documentation](https://scriptworker-scripts.readthedocs.io/en/latest/scriptworkers-local.html). The tl;dr is that you need a landoscript virtualenv, worker configuration file, and task.json.

It is recommended to run `pip install -e .` in the [`landoscript` directory](https://github.com/mozilla-releng/scriptworker-scripts/tree/master/landoscript) to install landoscript into the virtualenv. This will avoid the need to reinstall each time you make a change.

Your `worker.json` should look something like the following:
```
{
  "work_dir": "/home/bhearsum/tmp/landoscript-tests/work",
  "artifact_dir": "/home/bhearsum/tmp/landoscript-tests/artifacts",
  "verbose": true,
  "lando_api": "https://stage.lando.nonprod.webservices.mozgcp.net/api",
  "lando_token": "available in relengworker sops",
  "schema_file": "/home/bhearsum/repos/scriptworker-scripts/landoscript/src/landoscript/data/landoscript_task_schema.json",
  "treestatus_url: "https://treestatus.prod.lando.prod.cloudops.mozgcp.net",
  "github_config": {
	"privkey_file": "available in releng worker sops; see init-worker.sh for decoding instructions",
	"app_id": "1227773"
  },
  "poll_time": 30
}
```

The `app_id` above is that of the [releng-read-only-dev](https://github.com/apps/releng-read-only-dev) app, which is installed in the repositories that landoscript needs to function.

Your `task.json` will need to be placed inside the `work_dir`. You can start with the `payload` and `scopes` from a live landoscript task, and perhaps append `"dry_run": true` to it. For example:
```
{
  "scopes": ["project:releng:lando:repo:main.json", "project:releng:lando:action:l10n_bump"],
  "payload": {
    "actions": ["l10n_bump"],
    "lando_repo": "main.json",
    "ignore_closed_tree": true,
    "l10n_bump_info": [
      {
        "name": "Firefox l10n changesets",
        "path": "browser/locales/l10n-changesets.json",
        "ignore_config": {
          "ja": [
            "macosx64",
            "macosx64-devedition"
          ],
          "ja-JP-mac": [
            "linux",
            "linux-devedition",
            "linux64",
            "linux64-aarch64",
            "linux64-devedition",
            "linux64-aarch64-devedition",
            "win32",
            "win32-devedition",
            "win64",
            "win64-devedition",
            "win64-aarch64",
            "win64-aarch64-devedition"
          ]
        },
        "l10n_repo_url": "https://github.com/bhearsum/firefox-l10n",
        "platform_configs": [
          {
            "path": "browser/locales/all-locales",
            "platforms": [
              "linux",
              "linux-devedition",
              "linux64",
              "linux64-aarch64",
              "linux64-devedition",
              "linux64-aarch64-devedition",
              "macosx64",
              "macosx64-devedition",
              "win32",
              "win32-devedition",
              "win64",
              "win64-devedition",
              "win64-aarch64",
              "win64-aarch64-devedition"
            ]
          }
        ],
        "l10n_repo_target_branch": "main"
      },
      {
        "name": "Mobile l10n changesets",
        "path": "mobile/locales/l10n-changesets.json",
        "l10n_repo_url": "https://github.com/bhearsum/firefox-l10n",
        "platform_configs": [
          {
            "path": "mobile/android/locales/all-locales",
            "platforms": [
              "android",
              "android-arm",
              "android-multilocale"
            ]
          }
        ],
        "l10n_repo_target_branch": "main"
      }
    ],
    "dry_run": true
  }
}
```

Once you have all those things in place, you can run the following in the directory containing `worker.json` to execute the task:
```
artifact_dir="YOUR_ARTIFACT_DIR"
rm -rf $artifact_dir
landoscript worker.json
```

Depending on how you prefer to work, you may want to pipe the output to a file, or through `tee`. In either case, once the task is complete you can assess the result through a combination of:
* The exit code (`echo $?`)
* The log output
* The artifacts in your `artifact_dir`

Any landoscript task that would've submitted a change to a repository (or did, in the case of a non-dry run) will publish a `lando-actions.json` artifact containing the payload of the submission to Lando. Most landoscript tasks publish artifact artifacts containing things such as specific diffs to help assess their results.

## Testing on Try

In this section we will cover testing on Try. Non dry-run tasks involve a bit of extra set-up. If you're running dry-run tasks, simply skip the next section.

### Repository setup

When running non-dry run tasks you must ensure that [https://github.com/mozilla-releng/staging-firefox](
https://github.com/mozilla-releng/staging-firefox) is in a state where the branch you're testing on does not already have the changes that landoscript is expected to make. In most cases this can be achieved by resetting the branch to the current state of the upstream [https://github.com/mozilla-firefox/firefox](https://github.com/mozilla-firefox/firefox) repository. To do this, you'll need to force push that repository's branch to the staging repository with something like the following:
```
~/repos/firefox main *20 ❯ git remote -v | grep '\(upstream\|staging\)'
staging	git@github.com:mozilla-releng/staging-firefox.git (fetch)
staging	git@github.com:mozilla-releng/staging-firefox.git (push)
upstream	git@github.com:mozilla-firefox/firefox.git (fetch)
upstream	git@github.com:mozilla-firefox/firefox.git (push)
~/repos/firefox main *20 ❯ git push -f staging upstream/main:main        
To github.com:mozilla-releng/staging-firefox.git
 + d85abd381aa4...83b2199691c1 upstream/main -> main (forced update)
```

Note that depending on what your testing, you'll need to update different branches. (eg: testing a beta release will involve updating the `beta` branch). When testing `merge-automation` tasks, the `to_branch` is the one needs to in a good state.

You may also need to delete tags from the `staging-firefox` repository if your test is expected to create them.

If you have force pushed to any branch or deleted any tags you must poke the VCS folks and ask them to "delete the repo directory and restart tnhe automation worker" to clear out any now-stale refs or tags. (This will no longer be necessary after [this bug](https://bugzilla.mozilla.org/show_bug.cgi?id=1941013) is fixed.)

### Running landoscript tasks on Try

There are multiple ways to run landoscript tasks on Try. Below are recommendations for each task type.

#### android-l10n-import / android-l10n-sync / l10n-bump

Simply push to try with `./mach try fuzzy` and select one or both of the tasks. (Note that in production, `android-l10n-sync` only runs on `beta`, but the task is branch-agnostic, so running it from a `main` based Try push is generally OK.)

### release-early-tagging

Run a [staging release](staging-release) on a Try push; this task will run as soon as the `promote` phase is scheduled.

### release-version-bump

Run a [staging release](staging-release) on a Try push. Start the staging release at the `ship` phase. You can then use `taskcluster api queue scheduleTask $taskid` to immediately start the `release-version-bump` task. (Although this task has upstream dependencies, it does not fetch any artifacts from them - so this is safe to do.)


### merge-automation

Merge automation tasks can be tested by pushing to try with `./mach try empty` and using Custom Push Actions in Treeherder to run the task you want (see the [Merge Duty documentation for how to do this](merge_duty)). Take care to push to try from the branch the task would run on in production. For example, an `esr128` based branch when testing `bump-esr128`, or a `beta` based branch when testing `beta-to-release`.
