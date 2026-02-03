Test Taskgraph Changes in Gecko
================================

Testing Locally
---------------

To test upstream taskgraph changes in a Gecko repository, first make your changes in your local taskgraph repository. Then install that version into the Firefox virtualenv using:

::

   ./mach python --virtualenv taskgraph -m pip install -e /path/to/taskgraph

This will install your local taskgraph along with any new dependencies it may require. Now when you run ``./mach taskgraph``, it will use your local copy instead of a release from PyPI.

.. warning::

    When ``mach`` re-generates the virtualenvs, it will clobber your local install. If this happens you will need to re-install your local copy afterwards.

Testing on Try
--------------

To test taskgraph changes on Try, you need to modify the requirements file to point to your branch or pull request. This process is more involved than local testing.

1. Modify ``taskcluster/requirements.in`` to reference your taskgraph branch:

   ::

      taskcluster-taskgraph@git+https://github.com/user/taskgraph@refs/pull/123/head

2. Re-compile the requirements file without hashes:

   ::

      pip-compile --no-emit-index-url taskcluster/requirements.in

3. Disable hash verification by setting an environment variable in ``.taskcluster.yml``:

   ::

      PIP_REQUIRE_HASHES: 0

4. Push your changes to Try.

.. warning::

    This process currently requires removing the `--require-hashes flag from mach <https://searchfox.org/mozilla-central/source/python/mach/mach/site.py#1540>`__.

For more details, see the upstream documentation on `Testing Pre-Release Versions of Taskgraph <https://taskcluster-taskgraph.readthedocs.io/en/stable/howto/bootstrap-taskgraph.html#testing-pre-release-versions-of-taskgraph>`__.