L10n Cross-channel
==================

L10n cross-channel is a cron process in mozilla-central that we use to grab all the localizable en-US strings from all of our shipping Gecko trees, then push them to a `quarantine repo <https://hg.mozilla.org/l10n/gecko-strings-quarantine/>`_, after which a human can then review the commits and push them to the `non-quarantine repo <https://hg.mozilla.org/l10n/gecko-strings/>`_, where it populates strings in `Pontoon <https://pontoon.mozilla.org/>`_ for localizers to localize, after which the localized strings land in the appropriate `l10n repo <https://hg.mozilla.org/l10n-central/>`_.

How to adjust the times cross-channel runs
------------------------------------------

We specify the times in `.cron.yml <https://hg.mozilla.org/mozilla-central/file/335652eb938ddb0101b016b8e29b60feccdd24eb/.cron.yml#l327>`_. Change those times, commit, push to phab, get review, merge. The change won't take effect until the commit lands on mozilla-central.

How do I find cross-channel code
--------------------------------

The mach command comes from `tools/compare-locales/mach_commands.py <https://hg.mozilla.org/mozilla-central/file/335652eb938ddb0101b016b8e29b60feccdd24eb/tools/compare-locales/mach_commands.py#l117>`_.

The logic comes from `python/l10n/mozxchannel <https://hg.mozilla.org/mozilla-central/file/335652eb938ddb0101b016b8e29b60feccdd24eb/python/l10n/mozxchannel>`_.

How to adjust which repositories we look at for en-US strings
-------------------------------------------------------------

The repositories we look at are specified in `get_default_config <https://hg.mozilla.org/mozilla-central/file/335652eb938ddb0101b016b8e29b60feccdd24eb/python/l10n/mozxchannel/__init__.py#l19>`_, namely the ``heads`` we pull into the unified repositories.

How do I debug cross-channel
----------------------------

Use the ``./mach l10n-cross-channel`` command. This command takes a list of actions. The `prep <https://hg.mozilla.org/mozilla-central/file/335652eb938ddb0101b016b8e29b60feccdd24eb/tools/compare-locales/mach_commands.py#l224>`_ and `create <https://hg.mozilla.org/mozilla-central/file/335652eb938ddb0101b016b8e29b60feccdd24eb/tools/compare-locales/mach_commands.py#l298>`_ actions should create an outgoing patch of any new strings. (It may help to force this by setting a `quarantine repo URL <https://hg.mozilla.org/mozilla-central/file/335652eb938ddb0101b016b8e29b60feccdd24eb/python/l10n/mozxchannel/__init__.py#l22>`_ that is behind a number of commits, so we always have new strings to push.)

Sprinkle with some ``import pdb; pdb.set_trace()`` and you should be able to debug.
