Updating one ESR version to another
===================================

Overview
--------

When an ESR version is end-of-life'd we need to update still supported users to
the next ESR version. This usually happens with the x.3.0 release of the new ESR
version, eg: 78.3.0esr. The general steps to this process are the same every time
but the specifics change -- so it's important to check your work with other members
of the team, as well as RelMan, and for QA to test.

Figure out what rules are needed
--------------------------------

There's two things you need to know before you can determine what rule changes will be
needed:

1. Do we need to watershed at the final version of the older ESR?

2. Are there any platforms that the older ESR supports, that the newer one does not?

To answer the first question, look at the Firefox release channel rules on https://balrog.services.mozilla.com/rules?product=Firefox&channel=release. More specifically, you're looking for any rules with
a version specifier between the older ESR version and the newer ESR version, and that
are marked as a watershed (usually by the word "watershed" in the comment field).

To know whether ane platforms are being deprecated, talk to RelMan.

Adjust rules on the esr-localtest and esr-cdntest channels
----------------------------------------------------------

This may be as little as deleting one existing rule, or as much as creating multiple new rules,
depending on what you discovered in the previous section. This section will show examples
of everything that may need to happen.

Add platform deprecation rules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If any platform are being deprecated, you need to create two new rules (per channel). The first will allow
the deprecated users to update to their last support version, the second will block them from
updating past that version. For example, here is what we did for XP/Vista deprecation: |platform-deprecation|

Add a watershed rule
^^^^^^^^^^^^^^^^^^^^

If you need a watershed, you can re-use the existing rule for the older ESR version. Usually
these are aliased as something like ``esr68-localtest``. You will need to add a version filter
that catches any update requests less than the major version of the older ESR. For example,
the esr68 watershed rule set version to ``<68.0``, like so: |watershed|

Removing the older esr version rule
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you did _not_ need a watershed, you can simply delete the primary rule (the one with the alias)
for each test channel. For example, had esr68 not needed a watershed, we would've deleted the
``esr68-localtest`` and ``esr68-cdntest`` rules. Do not do this if a watershed is needed! Follow
the instructions in the previous section instead.

Test!
-----

You should do your own basic testing before handing off to QA. To test the esr68 watershed, we
did two things:

1. Verified that a 60.0esr url (such as https://aus5.mozilla.org/update/3/Firefox/60.0/20141202185629/Darwin_x86_64-gcc3-u-i386-x86_64/en-US/esr-localtest/default/default/default/update.xml), received an update to 68.12.0esr.

2. Verified that a 68.12.0esr url (such as https://aus5.mozilla.org/update/3/Firefox/68.12.0/20141202185629/Darwin_x86_64-gcc3-u-i386-x86_64/en-US/esr-localtest/default/default/default/update.xml) received an update to 78.3.0esr.

Platform deprecations are usually best left to QA to test. So now you can hand off to them, and ask
them to verify that the update paths are correct, and that platform deprecations are handled
appropriately.

Adjust esr channel rules
------------------------

After we ship the newer ESR version, we can carry the test channel rules that were made
over to the main esr channel. The simplest way to do this is to take the ``esr-cdntest``
rules you created or changed, and update them to have a channel of ``esr*`` - which will
cause them to apply to any channel starting with ``esr``. These will be subject to signoff.
Once they've been made live you should also delete the ``esr-localtest`` rules, as they
have been superceded by the new ``esr*`` rules.

.. |platform-deprecation| image:: /procedures/release-duty/desktop/platform-deprecation.png
.. |watershed| image:: /procedures/release-duty/desktop/watershed.png


The Snap case
-------------

In addition to Balrog, you need to update the Snap store too. For more information about Snap,
see `ubuntu-snap <ubuntu-snap.html>`__. Steps:

1. ``docker pull snapcore/snapcraft:stable``
2. ``docker run -ti snapcore/snapcraft:stable``
3. ``snapcraft login``. If you don't have credentials, use the team account.
4. ``snapcraft status firefox`` You should see this kind of output::

    Track    Arch    Channel    Version      Revision
    esr      amd64   stable     78.3.0esr-1  426
                    candidate  78.2.0esr-1  413
                    beta       ^            ^
                    edge       ^            ^
    latest   amd64   stable     80.0.1-1     418
                    candidate  81.0-2       425
                    beta       82.0b1-1     427
                    edge       ^            ^


5. ``snapcraft close firefox esr/candidate`` and you will get::

    Track    Arch    Channel    Version      Revision
    esr      amd64   stable     78.3.0esr-1  426
                    candidate  ^            ^
                    beta       ^            ^
                    edge       ^            ^

    The esr/candidate channel is now closed.


Bouncer and EOL'ing the old ESR branch
--------------------------------------

This includes a couple of things, before and after building/shipping X.3.0esr.

Before GTB of the X.3.0esr release
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. The new ESR branch needs to become the new default in a couple of
   places. (e.g. UV configs, Snap configs and bouncer aliases). For
   example, when we switched over to ESR78.3.0, we had to land `this`_
   on esr78 branch, in advance, to make sure the 78.3.0esr becomes both
   the ``current-esr`` and ``next-esr`` release returned by bedrock, we
   update the right Snap, etc.

2. The old ESR branch can be wiped off from
   central/beta/release/esr(NEW_ESR). During the 78.3.0 for example, we
   landed a patch similar to
   `this <https://phabricator.services.mozilla.com/D88618>`__ to remove
   all occurrences of esr68 and adjust configuration.

After X.3.0esr is shipped
^^^^^^^^^^^^^^^^^^^^^^^^^

1. Ship-it holds information that gets propagated to `product-details`_
   which is consumed dynamically by a bunch of places such as
   `bedrock`_. So whenever we move to the new ESR, while EOL-ing the old
   one, we also need to update the configurations in Ship-it. When
   78.3.0esr was released, we amended Ship-it `here`_.

2. Cron jobs in the new ESR branch need to have their configs adjusted
   so that they query against the correct value in bouncer. Until we
   branch ESR again, both current/next esr releases will point to a
   singular release so it needs to be properly updated to reflect the
   one one. For example once we shipped esr78, we pushed
   `this <https://phabricator.services.mozilla.com/D88619>`__ on esr78.

3. EOL-ing the old ESR branch. Once X.3.0 is shipped, we can stop
   generating CI for the old branch. That includes removing all the cron
   jobs, including but not limited to: periodic updates, nightlies,
   bouncer checks, searchfox, etc. For retiring and EOL-ing esr68 we’ve
   landed `this <https://phabricator.services.mozilla.com/D90994>`__.

4. Make sure to close the old ESR branch in `TreeStatus`_ as planned
   closure.

.. _this: https://phabricator.services.mozilla.com/D88591
.. _product-details: https://product-details.mozilla.org/1.0/firefox_versions.json
.. _bedrock: https://product-details.mozilla.org/1.0/firefox_versions.json
.. _here: https://github.com/mozilla-releng/shipit/pull/458
.. _TreeStatus: https://treestatus.mozilla-releng.net/static/ui/treestatus/
