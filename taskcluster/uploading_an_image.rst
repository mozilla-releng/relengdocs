.. _uploading_an_image:

Uploading an image
==================

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
