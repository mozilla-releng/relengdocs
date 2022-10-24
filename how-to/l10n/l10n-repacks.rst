L10n Repacks
============

We build Firefox desktop l10n repacks by taking a signed en-US package, exploding it, replacing its strings and dictionary with l10n strings and dictionary, and repacking it. We then sign the internals, package the internals, and sign the package as we do with Firefox desktop builds.

These repacks get their own section on archive.m.o, as well as their own balrog entries, partial updates, etc. etc.

How do we adjust how many locales get repacked per shippable-l10n task?
-----------------------------------------------------------------------

Modify the `locales-per-chunk <https://hg.mozilla.org/mozilla-central/file/1f961aaf191242ebb72c54b0090fe04c9f0f2467/taskcluster/ci/shippable-l10n/kind.yml#l40>`_ value. This is currently set to 5, which gives us ~20 l10n repack tasks per promote graph.

How do we change the list of locales to repack?
-----------------------------------------------

For Central and Beta, we do this through :ref:`l10n-bumper`. First, follow :ref:`l10n_bumper_platform_locale_change` to adjust the list of locales, then follow :ref:`manually_trigger_l10n_bumper`.

Once the l10n bump lands in central or beta, the list of locales has changed.

If this is for any other gecko branch, we likely don't run l10n bumper there, so manually editing `browser/locales/l10n-changesets.json <https://searchfox.org/mozilla-central/source/browser/locales/l10n-changesets.json>`_ should do the trick.

How do we figure out the specifics of l10n repack logic?
--------------------------------------------------------

This is likely diving into the logs and/or scripts+makefiles.

For the log approach, find a recent shippable-l10n task in Central, Beta, Release, or ESR.
We're using a mozharness script currently, which should be verbose about each of the commands it runs, e.g.::

    INFO - Running command: ['make', 'wget-en-US'] in /builds/worker/workspace/obj-build/browser/locales
    INFO - Copy/paste: make wget-en-US
    INFO - Using env: (same as previous command)

The kind config is in `taskcluster/ci/shippable-l10n/kind.yml <https://searchfox.org/mozilla-central/source/taskcluster/ci/shippable-l10n/kind.yml>`_. (The ``l10n`` kind is for on-change CI l10n to make sure developers don't break l10n per-push; the ``shippable-l10n`` kind is the one we ship.)

The script is `testing/mozharness/scripts/desktop_l10n.py <https://searchfox.org/mozilla-central/source/testing/mozharness/scripts/desktop_l10n.py>`_. It calls makefiles like `browser/locales/Makefile <https://searchfox.org/mozilla-central/source/browser/locales/Makefile.in>`_ and `toolkit/locales/l10n.mk <https://searchfox.org/mozilla-central/source/toolkit/locales/l10n.mk>`_.

These makefiles call `compare-locales <https://github.com/mozilla/compare-locales>`_, which we `vendor in-tree <https://searchfox.org/mozilla-central/source/third_party/python/compare_locales>`_.

.. Warning::
   The l10n Makefiles and logic were difficult to maintain or understand back when we had Makefile and l10n experts!

   Don't be surprised if they are difficult to debug or reason about, or if they create a roadblock to improving the build system in general.

If there is significant push to refactor or improve single locale repacks, we likely want to push on the `unrepack project <https://docs.google.com/document/d/1muouK8yKV14MFNqOqQ99G_ae834TJ6dGV0fZM1ilAx8/edit>`_ instead.
