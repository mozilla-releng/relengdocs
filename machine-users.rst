Machine Users
=============


Mercurial Users
---------------

Level 3
.......

ffxbld
   Used for version bumps and tagging of Firefox release.

   - scriptworker: gecko-3-tree

tbirdbld
   Used for version bumps and tagging of Thunderbird releases

   - scriptworker: comm-3-tree

ffxbld-merge
   Used for merge day automation for firefox. Restricted in what changes it can push
   `here <https://hg.mozilla.org/hgcustom/version-control-tools/file/tip/hghooks/mozhghooks/check/merge_day.py>`_.

   - scriptworker: gecko-3-tree


Level 1
.......

trybld
   Used for version bumps and tagging of staging releases

   - scriptworker: gecko-1-tree comm-1-tree

stage-ffxbld-merge
   Used for staging merge day automation. Restricted in what changes it can push
   `here <https://hg.mozilla.org/hgcustom/version-control-tools/file/tip/hghooks/mozhghooks/check/merge_day.py>`_.

   - scriptworker: gecko-1-tree

trybld-scriptworker
   Used for testing scriptworker tasks against newly deployed script versions.
   - firefoxci taskcluster secret: project/releng/scriptworker/scriptworker-canary-sshkey
