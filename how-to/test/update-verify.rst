=============
Update Verify
=============
Update verify is test that runs before each Firefox Release (excluding Nightlies) are shipped. Its main purpose is to ensure that users who receive the release through an update MAR end up in the same place as a fresh install would get them. This helps us to ensure that partial MARs work in future updates, and that code signatures are valid regardless of how a user arrived at a new version.

You can read more about `update verify in the Firefox Source Docs <https://firefox-source-docs.mozilla.org/tools/update-verify/index.html>`__.

------------------
Running it locally
------------------

~~~~~~~~~~~~~
Requirements:
~~~~~~~~~~~~~

- `Docker <https://docs.docker.com/get-docker/>`__
- [optional | Mac] zstd (`brew install zst`)

~~~~~~~~~~~~
Docker Image
~~~~~~~~~~~~

#. `Ship-it <https://shipit.mozilla-releng.net/recent>`__ holds the latest builds.

#. Clicking on "Ship task" of latest build will open the task group in Taskcluster.
#. On the "Name contains" lookup box, search for `release-update-verify-firefox` and open a `update-verify` task
#. Make note of the `CHANNEL` under Payload. ie: `beta-localtest`
#. Click "See more" under Task Details and open the `docker-image-update-verify` task.

Download the image artifact from *docker-image-update-verify* task and load it manually

::

    zstd -d image.tar.zst
    docker image load -i image.tar

**OR**

Load docker image using mach and a task

::

    # Replace TASK-ID with the ID of a docker-image-update-verify task
    ./mach taskcluster-load-image --task-id=<TASK-ID>

~~~~~~~~~~~~~~~~~~~~
Update Verify Config
~~~~~~~~~~~~~~~~~~~~

#. Open Taskcluster Task Group
#. Search for `update-verify-config` and open the task
#. Under Artifacts, download `update-verify.cfg` file

~~~~~~~~~~
Run Docker
~~~~~~~~~~

To run the container interactively:

* Replace `<MOZ DIRECTORY>` with gecko repository path on local host <br />
* Replace `<UVC PATH>` with path to `update-verify.cfg` file on local host. ie.: `~/Downloads/update-verify.cfg`
* Replace `<CHANNEL>` with value from `update-verify` task (Docker steps)

::

     docker run \
       -it \
       --rm \
       -e CHANNEL=beta-localtest \
       -e MOZ_FETCHES_DIR=/builds/worker/fetches \
       -e MOZBUILD_STATE_PATH=/builds/worker/.mozbuild \
       -v <UVC PATH>:/builds/worker/fetches/update-verify.cfg
       -v <MOZ DIRECTORY>:/builds/worker/checkouts/gecko \
       -w /builds/worker/checkouts/gecko \
       update-verify

> Note that `MOZ_FETCHES_DIR` here is different from what is used in production.

`total-chunks` and `this-chunk` refer to the number of lines in `update-verify.cfg`

::

     ./tools/update-verify/scripts/chunked-verify.sh --total-chunks=228 --this-chunk=4
