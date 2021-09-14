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
-  AMO needs the first ``listed`` version of an addon to be submitted
   via the admin web interface manually, the first time.

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

How To…
-------

How to handle New Languages for Release
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Context: the underlying issue for this lies within `issue_15353`_ and is on the roadmap to be fixed by AMO team.
Some relateed work is happening in H2 2021.

-  Once the promote phase is kicked off, any new language packs will
   fail the addon submission task, and require human intervention.
-  Go to the failed task, and look for its dependency on a nightly-l10n
   task, locally download the .xpi for the language in question.
-  Decrypt the AMO user/pass from our private repo, and in Firefox log
   into AMO’s Developer Hub (Private Browsing Mode recommended)
   [Screenshots `[1] <#01>`__ `[2] <#02>`__ `[3] <#03>`__ and
   `[4] <#04>`__]
-  Once there click over to ``My Addons`` and sort the list by “Created”
   (this brings the newest created addons to the top of the list)
   [Screenshots `[5] <#05>`__ `[6] <#06>`__ and `[7] <#07>`__]
-  Select the relevant language(s) to go to the extension detail page.
   `[Screenshot 8] <#08>`__
-  Select to Upload a new version, to see the following page
   `[Screenshot 9] <#09>`__
-  **IMPORTANT** On this page be SURE TO CLICK **CHANGE** to make the
   extension listed follow prompts to alter the input [Screenshots
   `[10] <#10>`__, `[11] <#11>`__, and `[12] <#12>`__]
-  Finally upload the .xpi with “Select a file…” and then you’ll see
   some results [Screenshots `[13] <#13>`__ and `[14] <#14>`__]
-  Continue
-  You’ll need to fill out a few required fields [Screenshots
   `[15] <#15>`__, `[16] <#16>`__ and `[17] <#17>`__]

   -  Summary can be simple “Language pack for ”
   -  License is to be set to MPL 2.0
   -  Submit this page with no further changes

-  In the slim chance you get hit with AMO’s restriction of path length,
   feel free to edit it in an attempt to be descriptive but within the
   limits, this is purely convenience. [Screenshot `[18] <#18>`__,
   `[19] <#19>`__]
-  Success! `[Screenshot 20] <#20>`__
-  Go back and rerun the addon submission task that failed, to unblock
   the release.

What if I don’t do the important step in the manual process above?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you forget to do the **CHANGE** to make the addon listed when
manually uploading it above. The release can still be unblocked, AMO
will see the requests and see “hey we have that version” and hand the
release process back the unlisted version. **HOWEVER** this means, the
new language pack will not be listed for this version of Firefox.

In order to make it listed we need a new build number (on a new
buildid), relman may be ok with waiting for another RC, or they may be
ok letting the new locale stay off AMO for the release cycle (until a
dot release), this is mostly a value judgment on which path forward.

Screenshots relevant to above
-----------------------------

01
~~

|Login Flow 1| `Back to how to
section <#how-to-handle-new-languages-for-release>`__ ### 02 |Login Flow
2| `Back to how to section <#how-to-handle-new-languages-for-release>`__
### 03 |Login Flow 3| `Back to how to
section <#how-to-handle-new-languages-for-release>`__ ### 04 |Login Flow
4| `Back to how to section <#how-to-handle-new-languages-for-release>`__
### 05 |Find Langpack Flow 1| `Back to how to
section <#how-to-handle-new-languages-for-release>`__ ### 06 |Find
Langpack Flow 2| `Back to how to
section <#how-to-handle-new-languages-for-release>`__ ### 07 |Find
Langpack Flow 3| `Back to how to
section <#how-to-handle-new-languages-for-release>`__ ### 08 |Details
Page| `Back to how to
section <#how-to-handle-new-languages-for-release>`__ ### 09 |Upload
Version Flow 1| `Back to how to
section <#how-to-handle-new-languages-for-release>`__ ### 10 |Upload
Version Flow 2| `Back to how to
section <#how-to-handle-new-languages-for-release>`__ ### 11 |Upload
Version Flow 3| `Back to how to
section <#how-to-handle-new-languages-for-release>`__ ### 12 |Upload
Version Flow 4| `Back to how to
section <#how-to-handle-new-languages-for-release>`__ ### 13 |Upload
Version Flow 5| `Back to how to
section <#how-to-handle-new-languages-for-release>`__ ### 14 |Upload
Version Flow 6| `Back to how to
section <#how-to-handle-new-languages-for-release>`__ ### 15 |Upload
Version Flow 7| `Back to how to
section <#how-to-handle-new-languages-for-release>`__ ### 16 |Upload
Version Flow 8| `Back to how to
section <#how-to-handle-new-languages-for-release>`__ ### 17 |Upload
Version Flow 9| `Back to how to
section <#how-to-handle-new-languages-for-release>`__ ### 18 |Adjust
Human URL 1| `Back to how to
section <#how-to-handle-new-languages-for-release>`__ ### 19 |Adjust
Human URL 2| `Back to how to
section <#how-to-handle-new-languages-for-release>`__ ### 20 |Success|
`Back to how to section <#how-to-handle-new-languages-for-release>`__

.. |Login Flow 1| image:: /addons/media/Screenshot_01.png
.. |Login Flow 2| image:: /addons/media/Screenshot_02.png
.. |Login Flow 3| image:: /addons/media/Screenshot_03.png
.. |Login Flow 4| image:: /addons/media/Screenshot_04.png
.. |Find Langpack Flow 1| image:: /addons/media/Screenshot_05.png
.. |Find Langpack Flow 2| image:: /addons/media/Screenshot_06.png
.. |Find Langpack Flow 3| image:: /addons/media/Screenshot_07.png
.. |Details Page| image:: /addons/media/Screenshot_08.png
.. |Upload Version Flow 1| image:: /addons/media/Screenshot_09.png
.. |Upload Version Flow 2| image:: /addons/media/Screenshot_10.png
.. |Upload Version Flow 3| image:: /addons/media/Screenshot_11.png
.. |Upload Version Flow 4| image:: /addons/media/Screenshot_12.png
.. |Upload Version Flow 5| image:: /addons/media/Screenshot_13.png
.. |Upload Version Flow 6| image:: /addons/media/Screenshot_14.png
.. |Upload Version Flow 7| image:: /addons/media/Screenshot_15.png
.. |Upload Version Flow 8| image:: /addons/media/Screenshot_16.png
.. |Upload Version Flow 9| image:: /addons/media/Screenshot_17.png
.. |Adjust Human URL 1| image:: /addons/media/Screenshot_18.png
.. |Adjust Human URL 2| image:: /addons/media/Screenshot_19.png
.. |Success| image:: /addons/media/Screenshot_20.png

Troubleshooting
---------------

These are the various ways in which addonscript can generally break when communicating with AMO. Because this initial draft is being written without directly seeing examples of bustage, the descriptions may be a bit rough. We can fill out "this error message means *this*" as we encounter them.

The initial meeting notes are `here <https://docs.google.com/document/d/1ANA-bJYHeWUTsU4wHMykZK73kqd_rdzkG3daWFGUUIw/edit#>`_.

Firefox version is not known
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Symptoms: TBD

Workaround: The AMO team submits new Firefox versions ahead of time.

Future fix: AMO team plans to add a privileged API for releng to create new versions.

Submitting a listed langpack for the first time
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Symptoms: TBD

Workaround: log in to AMO and submit the langpack through the website. This process will require adding some metadata that cannot currently be submitted through the API: license, version, etc.

This is `documented above <#how-to-handle-new-languages-for-release>`_.

Issues:

-  `error on submitting a new addon as channel=listed via the api #12709 <https://github.com/mozilla/addons-server/issues/12709>`_
-  `Add an API for releng to submit entirely new locales #15353 <https://github.com/mozilla/addons-server/issues/15353>`_

Future fix: add an API for releng to submit new locales, or auto-detect the user and langpack and do the right thing.

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

Refresh AMO API keys
~~~~~~~~~~~~~~~~~~~~
In order to submit the langpacks, we use API tokens from the addon
`scriptworker`_. The procedure to push is the same for both staging and production.
When the token needs to be refreshed, specific instructions on how
to do that lie within the ``amo-langpacks.yml`` in the SOPS global releng repo.

.. _issue_15353: https://github.com/mozilla/addons-server/issues/15353
.. _scriptworker: https://github.com/mozilla-releng/scriptworker-scripts/tree/master/addonscript
