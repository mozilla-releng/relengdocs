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

- inspect the image::

    docker inspect image_builder

This will give us a `RepoDigests` with the image digest sha256::

    "RepoDigests": [
        "mozillareleases/image_builder@sha256:e510a9a9b80385f71c112d61b2f2053da625aff2b6d430411ac42e424c58953f"
    ],

- push the image::

    docker push mozillareleases/image_builder:5.0.0

The sha256 from the output from this command is important should match the digest sha256 from the ``docker inspect`` command::

    (tgenv) akimoz: ~/src/gecko/mozilla-unified (4ee63a7) [11:47:39]
    10107$ docker push mozillareleases/image_builder:5.0.0
    The push refers to repository [docker.io/mozillareleases/image_builder]
    ba32b4fa8f05: Pushed
    5.0.0: digest: sha256:e510a9a9b80385f71c112d61b2f2053da625aff2b6d430411ac42e424c58953f size: 528

- land the change in-tree. This will look like [this](https://searchfox.org/mozilla-central/rev/ce21a13035623c1d349980057d09000e70669802/taskcluster/taskgraph/transforms/docker_image.py#36-40): note that the format is ``<account>/<name>:<version>@sha256:<image_digest_sha256>``.


decision images
---------------

At the time of writing, there are 2 decision images: a general one and mobile's. Both are built against the `taskgraph <https://treeherder.mozilla.org/jobs?repo=taskgraph>`__ repo.
They are only rebuilt whenever a change is detected by the decision task of taskgraph. You may want to upload them on DockerHub so that decision tasks that are using these images
can load them. The procedure is similar to the one above.

1. Load the image (see above)
2. Tag the image. Remove ``-mobile`` in the following command if you're dealing with the regular image::

    docker tag $IMAGE_ID mozillareleases/taskgraph:decision-mobile-$TC_INDEX_HASH

``$TC_INDEX_HASH`` is found in the routes of the taskcluster task that generated the image. Eg: ``$TC_INDEX_HASH`` is `5a222cefd6dd1397487a7b70f450a4ab16cf5eed71e126e34928b26d4ccf7577` when the route is ``index.taskgraph.cache.level-3.docker-images.v2.decision-mobile.hash.5a222cefd6dd1397487a7b70f450a4ab16cf5eed71e126e34928b26d4ccf7577``

3. Get the ``RepoDigests`` hash (see above).
4. Push the image::

    docker push mozillareleases/taskgraph:decision-mobile-$TC_INDEX_HASH

5. Check the digests match (see above)
6. Land the change in-tree. `See this example <https://github.com/mozilla-mobile/fenix/pull/16361/files#diff-a728f7e52d751b98eafa856e45594533339b44f229d7b83f930df335391e7e15R246>`__
