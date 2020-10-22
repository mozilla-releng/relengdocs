.. index::
    single: Rotate hg.m.o cert

Rotate hg.m.o cert
==================

The hg.m.o cert will next expire on 2021.10.31, and every year thereafter. We need to rotate the cert a month before it expires, to give us time to debug and resolve issues with the option of backing out. (During the 2020 cert rotation, we rotated the cert a week before it expired, and had to deal with multiple days of tree closures afterwards.)

2020 links
----------

- `Bug 1668017 <https://bugzilla.mozilla.org/show_bug.cgi?id=1668017>`_ is the original cert rotation bug.
- `Bug 1670712 <https://bugzilla.mozilla.org/show_bug.cgi?id=1670712>`_ and `bug 1671731 <https://bugzilla.mozilla.org/show_bug.cgi?id=1671731#c2>`_ track some of the fallout.

Steps
-----

- Create new cert (vcs team)
- Update the various fingerprint locations in-tree and in secrets (vcs team)
- Update treescript fingerprint, if applicable (releng team)
- Create trusted and untrusted docker-worker AMIs. The trusted AMIs need to have the CoT key. (taskcluster team)
- Create trusted and untrusted generic-worker AMIs. The trusted AMIs need to have the CoT key. (relops team)
- Land ci-configuration patches to use the new AMIs (taskcluster, relops, releng teams)
- Test, deal with fallout, update docs

We could use the opportunity to rotate CoT keys as well, in which case we would:

- generate new CoT keys before creating the new trusted AMIs
- add them to scriptworker
- release scriptworker
- roll out new scriptworker pools with the new scriptworker CoT key and the new trusted public keys in ``scriptworker.constants``
- then proceed with rolling out new AMIs
- remove the old CoT keys from ``scriptworker.constants`` once all trusted workers are using the new keys
