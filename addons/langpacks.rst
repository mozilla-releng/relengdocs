
Langpack Submission Pipeline
============================

Terminology:
------------

-  listed - Addon is viewable on AMO by end-users.
-  unlisted - Addon is available only to the addon uploader for
   download, and servable outside of AMO.
-  Language Pack - A translation pack for Gecko strings bundled as an
   addon.

Background
----------

Language packs now need to be signed (as of Gecko 60.1esr/61.0) to be
run inside of Firefox. In order to do that our release process submits
every language pack to AMO for signing.

Restrictions
~~~~~~~~~~~~

In order to achieve this we have to contend with a few current
restrictions of AMO itself, as well as Firefox the product, and
correlate them with our release process.

-  Version number of the language pack is baked into the language pack
   itself.
-  AMO only accepts one copy of each language pack for each specific
   version (a new upload needs a new version)
-  AMO does not support “promoting” an upload to ``listed`` if it was
   previously ``unlisted``

Process
~~~~~~~

-  Firefox, for every code check-in, builds an English (US) copy that is
   suitable for shipping to end users, as part of this build we generate
   the en-US language pack.
-  Once Release Management indicates we want to build a release, we
   kickoff the ‘promote’ phase of the release process, which starts the
   Localized Repackages, which generate each languages language pack.
-  The language packs get sent off to AMO on an addon submission task,
   this task submits and retries while it waits for AMO to sign the
   langpacks. Timing out (with a signal to retry the task) if needed.
-  The Addon Submission task is idempotent, so if a given langpack
   version is uploaded it will retrieve the same upload on subsequent
   calls (and resubmit any uploads which failed)
-  The Addon Submission task exposes the signed langpacks as task
   artifacts.
-  Beetmover moves the language packs to the release folder, allowing
   them to be easily downloaded by users not on AMO.

Troubleshooting
---------------

These are the various ways in which addonscript can generally break when communicating with AMO. Because this initial draft is being written without directly seeing examples of bustage, the descriptions may be a bit rough. We can fill out "this error message means *this*" as we encounter them.

The initial meeting notes are `here <https://docs.google.com/document/d/1ANA-bJYHeWUTsU4wHMykZK73kqd_rdzkG3daWFGUUIw/edit#>`_.

Submitting addons can be rate-limited
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Symptoms: Some langpack submissions fail, but some succeed. Reruns work after some time has passed.

Workaround: Rerun each failed task after waiting some time. Contact AMO about rate limiting for our user.

Current fix: Our current addonscript AMO user is supposed to bypass rate limiting checks. This should work unless something changes or breaks.

Intermittent errors
~~~~~~~~~~~~~~~~~~~

2020.08.24: a `langpack task <https://firefox-ci-tc.services.mozilla.com/tasks/J_VRZ2YWRU2Iyfwarovc3A/runs/0>`_ ran out of retries for ``bg`` and ``az``. A rerun fixed it::

    addonscript.exceptions.SignatureError: Expected 1 file. Got (0) full response:
    {
        'guid': 'langpack-bg@devedition.mozilla.org',
        'active': False,
        'automated_signing': True,
        'url': 'https://addons.mozilla.org/api/v3/addons/langpack-bg@devedition.mozilla.org/versions/81.0buildid20200824150741/uploads/43e64895a06348c588b088ef218ec211/',
        'files': [],
        'passed_review': False,
        'pk': '43e64895a06348c588b088ef218ec211',
        'processed': False,
        'reviewed': False,
        'valid': False,
        'validation_results': None,
        'validation_url': 'https://addons.mozilla.org/en-US/developers/upload/43e64895a06348c588b088ef218ec211',
        'version': '81.0buildid20200824150741'
    }

Permanent errors
~~~~~~~~~~~~~~~~

2022.11.28: All linux langpack tasks failed, but the osx langpack task succeeded. A rerun also failed.
Logs showed amo_put() produced HTTP status 409; subsequent amo_get()'s returned 404 until retries 
were exhausted and the task failed. Discussion with AMO devs on slack #addons revealed that they 
had recently added a version check to prevent submitting lower version numbers, which broke dot 
releases. To address this, `an exception was made for langpacks <https://github.com/mozilla/addons-server/issues/20029>`_. Once the fix was deployed to AMO, reruns of the failed langpack tasks succeeded.

2023.06.08: One linux langpack task `failed <https://bugzilla.mozilla.org/show_bug.cgi?id=1837547>`_.  Reruns also failed.  Logs showed amo_get() returned `'status': 'disabled'` for that file.  Discussion with AMO devs revealed that the langpacks for 114.0.1 and 115.0b3 were submitted around the same time, and AMO only allows a single version in each channel to be awaiting approval at one time - if a new version is uploaded before the previous one is approved and signed, the previous version is skipped and disabled.  SRE had to make AMO forget about that "disabled" version before a rerun could succeed.

Refresh AMO API keys
~~~~~~~~~~~~~~~~~~~~
In order to submit the langpacks, we use API tokens from the addon
`scriptworker`_. The procedure to push is the same for both staging and production.
When the token needs to be refreshed, specific instructions on how
to do that lie within the ``amo-langpacks.yml`` in the SOPS global releng repo.

.. _scriptworker: https://github.com/mozilla-releng/scriptworker-scripts/tree/master/addonscript
