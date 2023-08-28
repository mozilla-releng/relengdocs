Project Standards
=================

Release Engineering strives to use consistent tools and style conventions
across all projects. To that end, the `Release Engineering Project Standard`_
(or REPS) was created.

This repo contains both the REPS definition, as well as a tool that can be used
to bootstrap new projects that conform to this definition.

Standard Definition
-------------------

The standards themselves are defined in the `STANDARD.md`_ file at the root of
the repo.

Bootstrapping new Projects
--------------------------

The repo also provides a bootstrapping tool called ``reps-new``. The
recommended way to run it is with `pipx`_:

.. code-block:: bash

   $ pipx run reps-new

Updating the Standards
----------------------

These project standards are a living document, and it's encouraged that new
tools, workflows and modifications be added as our best practices evolve.

If you would like to adjust a standard, the recommended process is to:

1. `Create an issue`_ describing the change you'd like to make, share it with
   the team and get general consensus that it is worth making.
2. Create a PR that updates both `STANDARD.md`_ as well as the `cookiecutter`_
   templates used by ``reps-new``. These should ideally be done in the same
   commit.
3. If necessary, release a new version of ``reps-new``.
4. If necessary, update existing projects so they conform to the new standard.
   In general, we should strive to keep all projects synced with the latest
   standards, but this is not always possible in a timely manner due to
   conflicting priortities. So discretion can be used around the timeline for
   updating existing projects.

.. _Release Engineering Project Standard: https://github.com/mozilla-releng/reps
.. _STANDARD.md: https://github.com/mozilla-releng/reps/blob/main/STANDARD.md
.. _pipx: https://github.com/pypa/pipx
.. _Create an issue: https://github.com/mozilla-releng/reps/issues/new
.. _cookiecutter: https://cookiecutter.readthedocs.io/en/stable/
