.. _`status database`:

Status Database
~~~~~~~~~~~~~~~

http://hg.mozilla.org/build/buildbotcustom/file/a9f6adc7dcbb/status/db/model.py
https://wiki.mozilla.org/ReleaseEngineering/Buildbot_Database_Schemas

.. _finished:

finished jobs
+++++++++++++
When jobs complete, their information is stored into the status db.

Status of finished jobs is published to
http://builddata.pub.build.mozilla.org/buildjson/ from buildapi. TBPL
consumes http://builddata.pub.build.mozilla.org/buildjson/builds-4hr.js.gz
to find when jobs have completed.

