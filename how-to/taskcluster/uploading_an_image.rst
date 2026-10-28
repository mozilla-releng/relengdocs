.. _uploading_an_image:

Uploading an image
==================

image_builder
-------------

This assumes you have taskgraph installed in a virtualenv, you have docker installed and are logged in via ``docker login``, and you've already built the trusted docker image via a level 3 docker image task.

- load the image. Docker should be running; you should be logged into docker. Activate your taskgraph virtualenv and download+load the image::

    taskgraph load-image --task-id CDDoj06lSTSQ6qs5teT-CA

This will download public/image.tar.zst into docker.

- tag the image::

    docker tag image_builder mozillareleases/image_builder:5.0.0

- push the image::

    docker push mozillareleases/image_builder:5.0.0

- land the change in-tree, in both firefox and taskgraph. This will look like [this](https://searchfox.org/mozilla-central/rev/ce21a13035623c1d349980057d09000e70669802/taskcluster/taskgraph/transforms/docker_image.py#36-40): note that the format is ``<account>/<name>:<version>@sha256:<image_digest_sha256>``.


decision images
---------------

At the time of writing, there are 2 decision images: a general one and gecko's. The former is built against the `taskgraph <https://treeherder.mozilla.org/jobs?repo=taskgraph>`__ repo, while `gecko_decision` is built `in firefox <https://searchfox.org/firefox-main/source/taskcluster/docker/decision/>`__
They are only rebuilt whenever a change is detected by the respective decision task.  The upstream taskgraph image is uploaded automatically on each taskgraph release.  The `gecko_decision` image is uploaded periodically to DockerHub so that `.taskcluster.yml` can reference it.  The procedure is similar to the one above.

1. Load the image (see above)
2. Tag::

    docker tag decision:latest mozillareleases/gecko_decision:$VERSION

where ``$VERSION`` is the contents of ``taskcluster/docker/decision/VERSION`` (which should have been updated ahead of the image build).

3. Push the image::

    docker push mozillareleases/gecko_decision:$VERSION


4. Land the change in-tree. `See this example <https://github.com/mozilla-firefox/firefox/commit/9d75bf09384526297757675ec03a604000c657a5>`__

.. warning::

   If uploading an image that bumps the version of Mercurial being used, make
   sure to bump the `checkout cache version`_. See :ref:`missing Mercurial
   features` for more information.

.. _checkout cache version: https://searchfox.org/mozilla-central/rev/1ca8ea11406642df4a2c6f81f21d683817af568d/.taskcluster.yml#217


.. _build-decision-image:

build-decision image
--------------------

Usually this will only be needed for re-pinnning the requirements, or minor changes to the image running hooks.
If you don't have a token, you will need to login to dockerhub and create a CLI token. The credentials for mozillareleases user is in sops.

1. [optional] Re-pin the requirements::

    maintenance/pin.sh

2. Commit your changes, submit a PR, merge, wait for build-decision task to show up in the Github checks UI.
3. Load the image (see above).
4. Tag the image with your commit hash

    docker image tag build-decision mozillareleases/build-decision:86cc5419c32996b7d78422d7fed33ce79576f8eb

5. Push the image to dockerhub
6. Now you should be able to update the image URL in `hg-push-template <https://github.com/mozilla-releng/fxci-config/blob/main/hg-push-template.yml>`__ and `cron-task-template <https://github.com/mozilla-releng/fxci-config/blob/main/cron-task-template.yml>`__
