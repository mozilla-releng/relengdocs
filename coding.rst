=================
Coding Guidelines
=================

This section describes current (2014 May) practices. It will be the
basis for future changes.

All of the guidelines below are for new projects. For existing projects,
follow the current style or migrate the entire project to a newer
approach.

Code Storage
============

The most important thing is to have your code in VCS and somewhere other
than your laptop. Beyond that, you're free to develop wherever you want
using the tools you want. As something moves towards being deployable,
the master (Repository of Record - RoR) repository needs to meet the
following criteria, mostly based on deployment tool needs:

    Deployed via repository checkout:
        - Must be in either hg.mozilla.org (historical home), or
          git.mozilla.org (if git client installed on target).
        - Examples include buildbot code.

    Deployed via puppet:
        - Source should be in separate repository with documentation,
          tests, and other goodness.
        - Source repository should be \*.mozilla.org server.

            - Historically, some were (only) in end user repos on
              github.
        - Only a file (or other artifact) produced from the source
          repository should be deployed by puppet. Puppet only changes
          are discouraged.
        - Examples include tooltool script, buildapi sdist tarballs,
          custom MRTG tests.

    Other cases:
        - Handle as under "Deployed via puppet"
        - Examples? unknown

Scripting Languages
===================

1. Python is our tool of choice for anything significant or long lived.

    - PEP-8 is our guideline, except for line length.
    - if mozharness makes sense, prefer that.
    - prefer modules with entry points over scripts (works on Windows)

2. Bash scripts are acceptable for "pure unix" items like cronjobs.

3. Various legacy systems are in PHP or Perl. Let's not do that again
   without consent.

Configuration Formats
=====================

At the moment, the bulk of our tooling uses:

    - python syntax & constructs (buildbot)
    - JSON (for host descriptions, web APIs)
    - INI format (git, hg)

Web Application Frameworks
==========================

Ideally, "everything is a web service", so we can maximize self-service
opportunities.

- Flask is preferred for new work.

    - If your app works as a blueprint, we have more flexibility in
      deployment options. That is a good thing.
    - Examples include relengapi, ship it

- Pylons has been used.

    - Examples include buildapi

- Twisted

    - Examples include buildbot

Futures
=======

Here are some ideas we'd like to add in the future. If you need
something like this, ask around.

    - Vagrant/docker development (at least) environments.

        - Ideally part of source code repository.
        - Still working on how to set up multi-app environments.

    - Deployment Checklist

        - Build/test on commit requirements
        - Operations documentation.
