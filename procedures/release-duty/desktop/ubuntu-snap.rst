Desktop Snap Releases
=====================

Snap is a package format supported by Canonical. It's targeted to
support every Linux distribution but it's mainly available on Ubuntu at
the moment. We've made Firefox publicly available on
https://snapcraft.io/firefox since Firefox 59.0.

Channels used
-------------

The snap store comes with the concept of tracks (à la Google Play
Store). For more explanation about them, see
https://docs.snapcraft.io/reference/channels. Release promotion
automatically uploads to these tracks:

+----------------------------------------+--------------------+--------------+
| Brand name                             | Track              | Notes        |
+========================================+====================+==============+
| Firefox                                | ``candidate``      | A human      |
|                                        |                    | has to       |
|                                        |                    | manually     |
|                                        |                    | promote      |
|                                        |                    | the Snap     |
|                                        |                    | to the       |
|                                        |                    | ``stable``   |
|                                        |                    | channel      |
+----------------------------------------+--------------------+--------------+
| Firefox Beta                           | ``beta``           |              |
+----------------------------------------+--------------------+--------------+
| Firefox Developer Edition              | N/A                | Not          |
|                                        |                    | supported    |
|                                        |                    | yet          |
+----------------------------------------+--------------------+--------------+
| Firefox Nightly                        | N/A                | Not          |
|                                        |                    | supported    |
|                                        |                    | yet          |
+----------------------------------------+--------------------+--------------+
| Firefox ESR                            | ``esr`` aka        | We plan      |
|                                        | ``esr/stable``     | to use       |
|                                        |                    | ``esr        |
|                                        |                    | /candidate`` |
|                                        |                    | whenever     |
|                                        |                    | the next     |
|                                        |                    | major ESR    |
|                                        |                    | version      |
|                                        |                    | comes out    |
+----------------------------------------+--------------------+--------------+

Promote a snap to the ``stable`` channel
----------------------------------------

Who?
~~~~

Like for Google Play, Release Management is in change of deciding when
they want to fully ship a Snap. Release Management has access to the web
interface (and the CLI because credentials are the same) and performs
the release action (like Google Play). If needed, Release Engineering
can help.

When?
~~~~~

Because, there is no roll out mechanism, Snaps are shipped to the entire
population of a given channel. Unlike Google Play, we can roll back
users to previous version, if needed. However, downgrades aren't
supported internally in Firefox. Based on these facts, we should ship
when we have enough data of the stability on Linux.

How?
~~~~

The easy way: via web interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Connect to https://dashboard.snapcraft.io/snaps/firefox/. Your
   credentials will be asked, your 2FA code too. If it doesn't, 'select
   “Always” for “Require an authentication device”, and click “Update”'
   like explained `on this
   page <https://help.ubuntu.com/community/SSO/FAQs/2FA#How_do_I_add_a_new_authentication_device_and_start_using_2-factor_authentication.3F>`__.
2. On the left side, click on the release you want to ship.
3. On the “channel” section, click on the link “Release”. If brings you
   to a new page. If the page remains blank, reload it.
4. Check the ``stable`` box (leave the ``candidate`` one checked) and
   click on ``Release``.

The more complete one: via command line
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Install ``snapcraft``. The simplest way is via `docker <https://hub.docker.com/r/snapcore/snapcraft/>`__:
   ``docker pull snapcore/snapcraft:stable``, then
   ``docker run -ti snapcore/snapcraft:stable bash``
   * alternatively: ``apt-get install snapcraft``
2. ``snapcraft login``. Your credentials will be asked, your 2FA code
   too. If it doesn't, 'select “Always” for “Require an authentication
   device”, and click “Update”' like explained `on this
   page <https://help.ubuntu.com/community/SSO/FAQs/2FA#How_do_I_add_a_new_authentication_device_and_start_using_2-factor_authentication.3F>`__.
3. ``snapcraft status firefox`` outputs something like:

::

   Track    Arch    Channel    Version      Revision
   esr      amd64   stable     60.0.2esr-2  98
                    candidate  ^            ^
                    beta       ^            ^
                    edge       ^            ^
   latest   amd64   stable     60.0.1-2     89
                    candidate  60.0.2-1     97
                    beta       61.0b14-1    101
                    edge       ^            ^

1. Note the revision of the ``latest/candidate`` (aka ``candidate``)
   snap. In this example: ``97``
2. If you don't see the version you are expecting, list all available
   revisions by running ``snapcraft list-revisions firefox | head``
3. ``snapcraft release firefox $REVISION stable``, ``$REVISION`` being
   the number found in the previous (e.g.: ``97``).

How to manually push a snap to the store, in case automation failed?
--------------------------------------------------------------------

1. Install ``snapcraft`` and login (see previous paragraph)
2. ``snapcraft push target.snap --release $CHANNEL``, ``$CHANNEL`` being
   one of ``esr``, ``candidate``, ``beta``.
3. If you forgot ``--release`` in the previous command, you can still
   use ``snap release [...]`` (see previous paragraph) to make the snap
   available to a channel.

Refresh macaroons credentials
-----------------------------

Snaps operate via `macaroons`_ to authenticate requests against the
Store. These are used by k8s ``pushsnap`` scriptworkers to perform
operations with the snaps.

When the macaroons token expiry, they need to be refreshed. Specific
instructions on how to do that lie within the ``ubuntu-store.txt`` in
the private repo.

.. _macaroons: https://dashboard.snapcraft.io/docs/api/macaroon.html


Refreshing collaborators
------------------------

Every now and then we need to curate the list of contributors that can handle
the snaps. In order to for one to do so, please use the main RelEng account credentials
and hop on the `collaborators`_ page and make those adjustements.

.. _collaborators: https://dashboard.snapcraft.io/snaps/firefox/collaboration/
