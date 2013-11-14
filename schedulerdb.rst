Scheduler Database
==================
http://hg.mozilla.org/build/buildbot/file/b4673f1f2a86/master/buildbot/db/schema/tables.sql

https://wiki.mozilla.org/ReleaseEngineering/Buildbot_Database_Schemas

build requests
--------------

pending jobs
------------
Jobs are pending when they are marked as not complete in the DB, and no
master currently has them claimed.

TBPL_ fetches pending jobs from
https://secure.pub.build.mozilla.org/builddata/buildjson/builds-pending.js,
which is populated from
https://secure.pub.build.mozilla.org/buildapi/pending?format=json

running jobs
------------
Jobs are running when they are currently claimed by a master and are
running on a slave.

TBPL_ fetches pending jobs from
https://secure.pub.build.mozilla.org/builddata/buildjson/builds-running.js,
which is populated from
https://secure.pub.build.mozilla.org/buildapi/running?format=json
