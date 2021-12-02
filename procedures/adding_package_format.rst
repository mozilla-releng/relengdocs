
Adding a package format
=======================

There are some gotchas to pay attention to when adding a new package format, in
particular related to bouncer.

The `release-bouncer-check` and `cron-bouncer-check` tasks use the
configuration files in `testing/mozharness/configs/releases/bouncer_*.py`,
which include 2 kinds of products: versioned ones, and `-latest` ones.

Because the latter do not exist in bouncer until after the first release with
that package format is out, they should not be added to the `bouncer-check`
configs until after the first release with them is shipped.

For example, if a new format `foo` is added in the `96.0a1` nightly cycle:

* `Firefox-%(version)-foo` can be added to the `beta` and `release` configs
  at the same time

* `Firefox-beta-foo-latest` can't be added to `bouncer_firefox_beta.py` (and
  uplifted) until after `96.0b1` is released

* `Firefox-foo-latest` should be
  added and uplifted as soon as possible after `96.0` ships (so that if
  anything turns out to be wrong, `cron-bouncer-check` flags it ASAP), but not
  before (otherwise `release-bouncer-check` will fail and block the release).

