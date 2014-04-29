.. _`adding_repo_to_releng_rtfd_account`:

====================================================
Adding a new repo to Releng Account on Read-The-Docs
====================================================

At the moment, our approach is to:
    - Enable |rtfd| updates on the github copy of the repo.
    - Add repo to Releng Account on |rtfd|.
    - Assign maintainers to the repo on |rtfd|.

Pre-requisites
==============

Before you can add a repo you should:

    - Already have configured docs in the repo. (See XXX)
    - Successfully built docs locally. (See XXX)

You also need:

    - Access to RelEng passwords.
    - Admin access for repo to be added on github.

Enable RTFD updates on github
===============================

- Visit the 'settings' link for the repository.
- Choose the "Webhooks & Services" link.
- Click the "Configure services" button.
- Select "ReadTheDocs" from the service list.
- Enable the "Active" checkbox.
- Click the "Update Settings" button.
- Click the "Configure services" button again, and verify
    that "ReadTheDocs" is checked.

Add repo to Releng Account on RTFD
==================================

Set up the doc project for the repository:

    - Log in to |rtfd| as user ``moz_releng``.
    - Click the "Import" button.
    - Fill in a name -- names are globally unique on all of rtfd.org, so
      we've been prefixing with "moz releng".
    - Fill in the URL it should pull from.
    - Click the "Create" button. You should see a message that your
      documentation is being built.

Add the new doc project as a subproject to the main project:

    - Click the "Dashboard" link.
    - Click the "Admin" button for the "moz releng docs" project.
    - Follow the "Subprojects" link.
    - Add the new project as a subproject, and click "Submit".


Assign maintainers to the repo on RTFD
======================================

- Log in to |rtfd| as user ``moz_releng`` (or yourself, if you're
  already a maintainer of the repository in question).
- From the dashboard, click the "Admin" link for the repository.
- Follow the "Maintainers" link.
- Add the |rtfd| user names to be admins of this repo's documents

.. |rtfd| replace:: `rtfd.org`_
.. _`rtfd.org`: http://moz-releng-docs.readthedocs.org/
