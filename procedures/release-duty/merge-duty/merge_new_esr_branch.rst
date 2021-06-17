Merge Duty for major ESR bump
=============================

Intro
-----

This manual describes how to set up a new ESR branch. The same process
can be applied for any branch set up, with slight modifications.

Example tracking bug: `Bug 1644817 - [meta] Support ESR78
<https://bugzilla.mozilla.org/show_bug.cgi?id=esr78>`__

Internal changes
----------------

This section covers changes to buildbot-configs and tools.

See `Bug 1646588 <https://bugzilla.mozilla.org/show_bug.cgi?id=1646588>`__
for the details and example changes.

tools changes
~~~~~~~~~~~~~

-  copy the old patcher config, so we can generate partial updates
   against the previous ESR release. (Not sure if this applies anymore?)
-  add new esr lines to l10n cross-channel `here <https://hg.mozilla.org/integration/autoland/rev/8bcf35827a03386d64e4b89b5b3136bb848b77fe#l1.42>`__ and `here <https://hg.mozilla.org/integration/autoland/rev/8bcf35827a03386d64e4b89b5b3136bb848b77fe#l1.55>`__.

External systems
----------------

CI relies on multiple systems, supported by different teams. File bugs
in advance to make sure other teams have enough time to address the
issue. Usually starting the whole process 2 weeks in advance of release
builds (3 weeks before the release), gives enough time to everybody.

Tasks
-----

Below is the list of bugs filed as a part of the ESR52 cycle. Go through
the list and verify that they are still valid for this ESR cycle and
clone them if needed.

(We may want to look at the dependencies for the `esr78 cycle <https://bugzilla.mozilla.org/show_bug.cgi?id=1644817>`__ for a more recent set.)

+---------------------------+------------------------------------------+
| Bug                       | Title                                    |
+===========================+==========================================+
| `1333745 <https:          | Please add tracking-thunderbird_esr52    |
| //bugzilla.mozilla.org/sh | and status-thunderbird_esr52 to the      |
| ow_bug.cgi?id=1333745>`__ | tracking flags                           |
+---------------------------+------------------------------------------+
| `1335870 <https:          | please create tracking-firefox-esr52 and |
| //bugzilla.mozilla.org/sh | status-firefox-esr52 flags               |
| ow_bug.cgi?id=1335870>`__ |                                          |
+---------------------------+------------------------------------------+
| `1337061 <https:          | Add mozilla-esr52 and comm-esr52 to      |
| //bugzilla.mozilla.org/sh | release_repositories                     |
| ow_bug.cgi?id=1337061>`__ |                                          |
+---------------------------+------------------------------------------+
| `1337066 <https:          | Please clone releases/mozilla-beta to    |
| //bugzilla.mozilla.org/sh | releases/mozilla-esr52                   |
| ow_bug.cgi?id=1337066>`__ |                                          |
+---------------------------+------------------------------------------+
| `1337087 <https:          | update tree closure hooks for            |
| //bugzilla.mozilla.org/sh | mozilla-esr52                            |
| ow_bug.cgi?id=1337087>`__ |                                          |
+---------------------------+------------------------------------------+
| `1337090 <https:          | Add mozilla-esr52 and comm-esr52 to      |
| //bugzilla.mozilla.org/sh | treeherder                               |
| ow_bug.cgi?id=1337090>`__ |                                          |
+---------------------------+------------------------------------------+
| `1337091 <https:          | Add mozilla-esr52 and comm-esr52 to      |
| //bugzilla.mozilla.org/sh | treestatus                               |
| ow_bug.cgi?id=1337091>`__ |                                          |
+---------------------------+------------------------------------------+
| `1337093 <https:          | Add mozilla-esr52 and comm-esr52 to      |
| //bugzilla.mozilla.org/sh | orange factor                            |
| ow_bug.cgi?id=1337093>`__ |                                          |
+---------------------------+------------------------------------------+
| `1337366 <https:          | Gecko-specific changes to support        |
| //bugzilla.mozilla.org/sh | mozilla-esr52                            |
| ow_bug.cgi?id=1337366>`__ |                                          |
+---------------------------+------------------------------------------+
| `1337489 <https:          | HTTP 500 for all trees view due to       |
| //bugzilla.mozilla.org/sh | missing comm-esr52 repo                  |
| ow_bug.cgi?id=1337489>`__ |                                          |
+---------------------------+------------------------------------------+
| `1339057 <https:          | Please add the approval-esr52 flag       |
| //bugzilla.mozilla.org/sh |                                          |
| ow_bug.cgi?id=1339057>`__ |                                          |
+---------------------------+------------------------------------------+
| `1339074 <https:          | Add mozilla-esr52 to the various lists   |
| //bugzilla.mozilla.org/sh | in repository.py                         |
| ow_bug.cgi?id=1339074>`__ |                                          |
+---------------------------+------------------------------------------+
| `1339076 <https:          | Make sure the right hooks are running on |
| //bugzilla.mozilla.org/sh | mozilla-esr52                            |
| ow_bug.cgi?id=1339076>`__ |                                          |
+---------------------------+------------------------------------------+
| `1339832 <https:          | Buildbot specific changes to enable      |
| //bugzilla.mozilla.org/sh | mozilla-esr52                            |
| ow_bug.cgi?id=1339832>`__ |                                          |
+---------------------------+------------------------------------------+
| `1340669 <https:          | Update merge day and esr docs            |
| //bugzilla.mozilla.org/sh |                                          |
| ow_bug.cgi?id=1340669>`__ |                                          |
+---------------------------+------------------------------------------+
| `1341330 <https:          | Please add mozilla-esr52 to DXR          |
| //bugzilla.mozilla.org/sh |                                          |
| ow_bug.cgi?id=1341330>`__ |                                          |
+---------------------------+------------------------------------------+
| `1341491 <https:          | Set ESR_NEXT in ship-it config           |
| //bugzilla.mozilla.org/sh |                                          |
| ow_bug.cgi?id=1341491>`__ |                                          |
+---------------------------+------------------------------------------+
| `1342117 <https:          | Set watch_all_branches to True for ESR52 |
| //bugzilla.mozilla.org/sh |                                          |
| ow_bug.cgi?id=1342117>`__ |                                          |
+---------------------------+------------------------------------------+
| `1342204 <https:          | Enable TC on mozilla-esr52               |
| //bugzilla.mozilla.org/sh |                                          |
| ow_bug.cgi?id=1342204>`__ |                                          |
+---------------------------+------------------------------------------+
| `1342431 <https:          | Turn off TC-based Android jobs on ESR52  |
| //bugzilla.mozilla.org/sh |                                          |
| ow_bug.cgi?id=1342431>`__ |                                          |
+---------------------------+------------------------------------------+
| `1343097 <https:          | Add mozilla-esr52 and comm-esr52 to      |
| //bugzilla.mozilla.org/sh | release-notifications heroku app         |
| ow_bug.cgi?id=1343097>`__ |                                          |
+---------------------------+------------------------------------------+
| `1343366 <https:          | browser_parsable_css.js fails on ESR52   |
| //bugzilla.mozilla.org/sh | ASAN builds due to the ESR branding      |
| ow_bug.cgi?id=1343366>`__ | changes                                  |
+---------------------------+------------------------------------------+

Merge
-----

Once mozilla-release is merged from mozilla-beta you can run the script
which pulls last changes from mozilla-release, updates some configs and
replaces some branding bits.

Running gecko_migration.py for mozilla-esr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The script will tag mozilla-release. It will continue by pulling
mozilla-release to mozilla-esrNN, adjusting branding and changing some
configs. Once the script finishes, run an hg diff to see the uncommitted
changes that the script generated:

::

   ESR_VERSION=51
   # checkout mozharness from the gecko tree using archiver
   # (We may want to just use mozharness in-tree if we have a mozilla-unified
   #  clone handy)
   wget https://hg.mozilla.org/build/tools/raw-file/default/buildfarm/utils/archiver_client.py
   python archiver_client.py mozharness --destination mozharness-esr$ESR_VERSION \
     --repo releases/mozilla-esr$ESR_VERSION --rev default --debug
   # run the script
   python mozharness-esr$ESR_VERSION/scripts/merge_day/gecko_migration.py \
     -c merge_day/release_to_esr.py
   hg -R build/mozilla-esr$ESR_VERSION diff
   python mozharness-esr$ESR_VERSION/scripts/merge_day/gecko_migration.py -c \
     merge_day/release_to_esr.py --commit-changes --push

The push should be available at Treeherder.

In case of failure, you can start again from the top; no need to clobber
(the on-by-default clean-repos action will be sufficient). It should be
faster the second time, since you won’t be pulling in as many changesets
from hg.m.o.

Release builds
--------------

Make sure to run a staging release.

Update this documentation
-------------------------

Keep this documentation up to date.

Ship it!
--------

Close the bug and have some tea. :)
