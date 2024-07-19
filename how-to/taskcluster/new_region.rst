.. new_region:

Adding a new region
===================

Adding a new GCP region for taskcluster workers requires changes in several places.

For gecko and comm pools:

- if the workers are going to clone the mercurial repository, add clonebundles in that region (e.g. https://bugzilla.mozilla.org/show_bug.cgi?id=1868861)
- if they're going to run builds, create sccache buckets and service accounts (e.g. https://bugzilla.mozilla.org/show_bug.cgi?id=1882374) and add the service accounts to the taskcluster configuration (e.g. https://mozilla-hub.atlassian.net/browse/SVCSE-2126)

For all pools:

- add the region and its zones to the relevant environments (e.g. https://github.com/mozilla-releng/fxci-config/commit/3230da41da284a8e58ed98ab225025b589e42370)
- add a test pool to validate things are working (e.g. https://github.com/mozilla-releng/fxci-config/commit/d576103d08e418ff454a520d5ab9e30505288ba4) using a try push (or PR)
- if any in-tree changes were necessary to get tasks to work in the new region, get them uplifted to all relevant branches
- finally, add the region to the relevant pool configurations
