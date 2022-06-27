Manually Beetmove Files
=======================

This is fairly rough documentation for a fairly rare request: beetmoving arbitrary artifacts into archive.m.o.

Links
-----

- https://github.com/mozilla-releng/beetmove-telemetry - Mihai had originally written this to help beetmove some glean files; Aki then added the apidocs for `Bug 1727585 <https://bugzilla.mozilla.org/show_bug.cgi?id=1727585>`_ and moved his fork into the mozilla-releng org for posterity.

Steps
-----

1. Identify what needs to beetmoved, and where.

  We're going to be pushing files to archive.m.o, which lends it some legitimacy: let's make sure this is a valid request.

  Generally we want to upload to an existing directory structure, e.g. https://archive.mozilla.org/pub/firefox/nightly/ or https://archive.mozilla.org/pub/mobile/toolchains/ or the like. If we need a new directory structure, we should coordinate with Product Delivery to make sure we have the right permissions and the right cleanup rules set.

2. Fork/clone the `repo <https://github.com/mozilla-releng/beetmove-telemetry>`_.

2. Determine which bucket and AWS creds are needed.

  For the bucket, look at the appropriate `production beetmoverscript configs <https://github.com/mozilla-releng/scriptworker-scripts/blob/e1609f9a0e384b870871717fa0306212b152b2e4/beetmoverscript/docker.d/worker.yml>`_. For instance, as of this writing, Firefox files go in the `net-mozaws-prod-delivery-firefox <https://github.com/mozilla-releng/scriptworker-scripts/blob/e1609f9a0e384b870871717fa0306212b152b2e4/beetmoverscript/docker.d/worker.yml#L54-L74>`_ bucket.

  Then go to the appropriate worker in k8s-sops (e.g. firefoxci-gecko-3), and grab the appropriate id and key. You'll need these to have write access to the bucket.

  Note: you probably want to use the appropriate staging bucket and staging id+key for testing first, so also grab those. These will be in use by the non-prod dep and/or dev pools.

  Copy the `config_example.json <https://github.com/mozilla-releng/beetmove-telemetry/blob/main/config_example.json>`_ file to ``config.json`` and edit it. In the example, ``maven-staging`` and ``maven-production`` our the script's nicknames. The ``buckets`` dict contains the real bucket name, along with a 2nd nickname which is hardcoded in the script, and the ``credentials`` dict holds the AWS creds.

3. Hack the script. Adding a ``--noop`` or ``--dry-run`` flag so you can test as much as possible without moving any files is recommended. If you aren't confident in the script, a test push to the staging bucket is recommended.

  Note: the script assumes you have the files downloaded locally. If you need to dynamically download a file, or if you need to download e.g. 6 months of nightlies a la `Bug 1727585 <https://bugzilla.mozilla.org/show_bug.cgi?id=1727585>`_, you may want to add automation to do that (and you probably want to verify the downloaded files' checksums via the chain-of-trust.json artifact for robustness and correctness).

4. Give it a real try, using the staging bucket. If that works, then if everyone's sure that the files and paths are correct, then push to the production bucket and close the bug.
