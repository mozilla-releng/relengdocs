A word on selecting partials in Ship-it
=======================================

This is purely informative as this is step performed by RelMan. Yet,
it’s good to have it at hand in case we’re asked. When selecting
partials in `Ship-it v2 <https://shipit.mozilla-releng.net/>`__, you
need to make sure those specific releases lie within both the
``candidates`` and ``releases`` directories. This is because
`release-runner <hg.mozilla.org/build/tools/file/tip/buildfarm/release/release-runner3.py>`__
is running some sanity checks on each of the provided partials. Part of
the checks make sure that the certain release has been fully pushed to
``~candidates`` directory and then copied-over into the ``~releases``
directory. Absent this and the `Ship-it
v2 <https://shipit.mozilla-releng.net/>`__ interface will throw an
error.

A note on rerunning action tasks
================================

Ocassionally action tasks fail for various reasons (e.g. scope issues).
Whenever the fix is done and you’re ready to rerun the action task, make
sure you cancel the previous run first. Otherwise, you’ll end up with
duplicates tasks within the same graph (e.g. ``push`` phase run twice
ends up with two tasks of ``push_to_releases``). Most of the tasks are
idempotent, but to minimize any possible negative outcome, *remember to
cancel before rerun*. On the same page, it’s worth noting that in some
cases, it’s just better **not to** rerun an action task, if some of the
tasks that it had created, had already ran. In this case it’s easier to
just burn a version number and respin another build number release.
