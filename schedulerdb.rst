.. _`scheduler database`:

Scheduler Database
~~~~~~~~~~~~~~~~~~
http://hg.mozilla.org/build/buildbot/file/b4673f1f2a86/master/buildbot/db/schema/tables.sql

https://wiki.mozilla.org/ReleaseEngineering/Buildbot_Database_Schemas

.. _`build requests`:

build requests
++++++++++++++

The buildrequests table in the schedulerdb is one of the core tables for
buildbot. buildbot masters use this table to find new jobs to run (with
`get_unclaimed_buildrequests`_)

Column documentation:

- `buildername`: this corresponds directly to the buildbot buildername.
    masters poll the table looking for pending jobs for builders they have
    enabled.

.. index:: builderPriority

- `priority`: this affects the order in which pending build requests are
    processed. See :ref:`builderPriority`

- `claimed_at`: this is a unix timestamp. masters update this field
    periodically as a job is running. It is *not* when the job starts. If a
    master dies or hangs, it will no longer be updating this field, and so
    other masters will be free to steal the job.

- `claimed_by_name`: The master's hostname and path that has this job
    claimed. This and `claimed_by_incarnation` are used to determine when
    requests can be stolen.

- `claimed_by_incarnation`: The master's process id and timestamp of when
    the process started. If a master sees requests that are claimed by itself
    (`claimed_by_name`), but a different `claimed_by_incarnation`, then it
    knows that it can immediately steal the request instead of waiting for
    the timeout.

- `complete`: Set to 1 if the build is complete

- `results`: The result code of the build. RETRY doesn't appear here,
    rather the build is set as unclaimed again.

- `submitted_at`: Timestamp when this request was submitted.

- `complete_at`: Timestamp when this request finished.



pending jobs
++++++++++++
Jobs are pending when they are marked as not complete in the DB, and no
master currently has them claimed.

TBPL fetches pending jobs from
https://secure.pub.build.mozilla.org/builddata/buildjson/builds-pending.js,
which is populated from
https://secure.pub.build.mozilla.org/buildapi/pending?format=json

running jobs
++++++++++++
Jobs are running when they are currently claimed by a master and are
running on a slave.

TBPL fetches pending jobs from
https://secure.pub.build.mozilla.org/builddata/buildjson/builds-running.js,
which is populated from
https://secure.pub.build.mozilla.org/buildapi/running?format=json

.. _get_unclaimed_buildrequests:
    http://hg.mozilla.org/build/buildbot/file/d1b5af18f350/master/buildbot/db/connector.py#l824
