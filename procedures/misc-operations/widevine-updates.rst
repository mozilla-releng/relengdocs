Widevine updates
================

Widevine is a system addon allowing Firefox users to read DRM'd content
(like Netflix). We provide updates via Balrog.

When
----

The request comes from the media team. They usually file a bug like
`this one. <https://bugzilla.mozilla.org/show_bug.cgi?id=1758423>`__

Sometimes updates must be done because Google (the owner of Widevine)
deprecates a version that still may be used by a supported Firefox
version (e.g.: Firefox ESR).

How
---

Ensure what Firefox version is able to run the new version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:warning: There are 2 types of patches the Media team makes:

1. The actual patch to make Firefox compatible with the new API (for
   example: `bug
   1420836 <https://bugzilla.mozilla.org/show_bug.cgi?id=1420836>`__).
   This kind of patch must happen **before** the balrog rule is set.
2. Another patch that updates the fallback downloader (like `bug
   1479579 <https://bugzilla.mozilla.org/show_bug.cgi?id=1479579>`__).
   This kind of patch can be landed **after** the balrog rule is set

Take a look at Widevine version numbers to determine whether Firefox
needs to be updated.

Old schema (< 1.4.9.X)
^^^^^^^^^^^^^^^^^^^^^^

For instance: 1.4.9.1088.

+-------+-----------+-----------------------------------------------------+
| Digit | Name      | Notes                                               |
+=======+===========+=====================================================+
| 1     | Major     | It has always been 1, so far                        |
+-------+-----------+-----------------------------------------------------+
| 4     | Module    | Significant changes must happen on the Firefox side |
+-------+-----------+-----------------------------------------------------+
| 9     | Interface | If this number changes, some Firefox internals must |
|       |           | be changed                                          |
+-------+-----------+-----------------------------------------------------+
| 10    | Revision  | This number keeps increasing even if the other      |
| 88    |           | numbers got bumped                                  |
+-------+-----------+-----------------------------------------------------+

If the API level (or higher) is bumped, please check with the Media team
what Firefox is able to run this Widevine.

New schema (> 1.4.9.x)
^^^^^^^^^^^^^^^^^^^^^^

For instance: TBD

===== ========= ==============
Digit Name      Notes
===== ========= ==============
\     Major     See old schema
\     Interface See old schema
\     Revision  See old schema
\     ?         TBD
===== ========= ==============

Create the blob
~~~~~~~~~~~~~~~

Unlike Firefox, no automation creates a blob. Nor do we have a script
(patch welcome!) to generate one. Therefore we need to create a new
blob. The easiest way to do this is to download the most recent
release blob,
e.g.\ `Widevine-1.4.9.1088 <https://aus4-admin.mozilla.org/releases/Widevine-1.4.9.1088>`__.
Then open in an editor. It's small and should be like:

.. code:: json

   {
     "hashFunction": "sha512",
     "name": "Widevine-4.10.2391.0",
     "product": "Widevine",
     "schema_version": 1000,
     "vendors": {
       "gmp-widevinecdm": {
         "platforms": {
           "Darwin_aarch64-gcc3": {
             "fileUrl": "https://redirector.gvt1.com/edgedl/widevine-cdm/4.10.2391.0-mac-arm64.zip",
             "filesize": 6511203,
             "hashValue": "041a9bbe89160f604d72db92fc9c1fdce75d528706245c837d4d0ea71e96c1b5106e512ca37e075373ceaeda64e6dd42e02889edaee8dc3077718620a16b4f2e"
           },
           "Darwin_x86_64-gcc3": {
             "alias": "Darwin_x86_64-gcc3-u-i386-x86_64"
           },
           "Darwin_x86_64-gcc3-u-i386-x86_64": {
             "fileUrl": "https://redirector.gvt1.com/edgedl/widevine-cdm/4.10.2391.0-mac-x64.zip",
             "filesize": 6942023,
             "hashValue": "2cf195a99dd13019c2f29e036f98e10905d1472f013970bd8b2f0ff65fe2b20a9058570c57b3595c1b9824326ac11a185a80008d618c673736323355345d69fe"
           },
           "Linux_x86_64-gcc3": {
             "fileUrl": "https://redirector.gvt1.com/edgedl/widevine-cdm/4.10.2391.0-linux-x64.zip",
             "filesize": 6328796,
             "hashValue": "8ce16faae96274e1f5ec63f6f543fa33ab3b7d469e59fac2d8b45cb27d3c95820cf80cd362d6e972a1c3c27e5c1b28c018fbdc2bb7df50f095391a646e277a99"
           },
           "Linux_x86_64-gcc3-asan": {
             "alias": "Linux_x86_64-gcc3"
           },
           "WINNT_aarch64-msvc-aarch64": {
             "alias": "WINNT_x86-msvc"
           },
           "WINNT_x86-msvc": {
             "fileUrl": "https://redirector.gvt1.com/edgedl/widevine-cdm/4.10.2391.0-win-ia32.zip",
             "filesize": 6331242,
             "hashValue": "24569de210f6a6d47daf0e64441f0c575dcbb23e5ff2fcb705edcd6e0fce9378caafd84e81a1c0efd25056a686ab8cb47855f43230ee37ddabc97453b72024ff"
           },
           "WINNT_x86-msvc-x64": {
             "alias": "WINNT_x86-msvc"
           },
           "WINNT_x86-msvc-x86": {
             "alias": "WINNT_x86-msvc"
           },
           "WINNT_x86_64-msvc": {
             "fileUrl": "https://redirector.gvt1.com/edgedl/widevine-cdm/4.10.2391.0-win-x64.zip",
             "filesize": 6537814,
             "hashValue": "81b2329d38a9370afc490db805a05c4b506b113ebd00f4e488bca97fd96267d92cb477e3a635880464ca66ed32f448e46ad3645f6af072547b5f09100db2bf74"
           },
           "WINNT_x86_64-msvc-x64": {
             "alias": "WINNT_x86_64-msvc"
           },
           "WINNT_x86_64-msvc-x64-asan": {
             "alias": "WINNT_x86_64-msvc"
           }
         },
         "version": "4.10.2391.0"
       }
     }
   }

From the above, edit the ``name``, ``version`` to match the current new
version. Then under each platform, update the ``hashValue``,
``filesize``, and ``fileUrl`` based on the values provided to you in the
widevine tracking bug. e.g. `bug
1475260 <https://bugzilla.mozilla.org/show_bug.cgi?id=1475260#c0>`__.

Finally, save that new release blob, upload it to Balrog via the “Add
new release” button within https://aus4-admin.mozilla.org/releases, and
save the release blob name to match the new version the blob is based
on.

Create the balrog rule
~~~~~~~~~~~~~~~~~~~~~~

Unlike Firefox updates, Widevine ones all happen in the same channel
(except for the nightlytest, the internal testing channel). This means
users are given a new widevine based on their Firefox version. For
instance: if we provide a new widevine to 62.0 at the time 62.0b15
ships, then users with 62.0b1-b14 will also get this version. Make sure
with the media team these betas are compatible! In the case it's not,
please remember Firefox doesn't send which beta it's on to Balrog. You
have to filter out based on the version **and** the buildID (the buildID
alone doesn't work if a 61 dot release happens afterwards).

In the end, a rule looks that filters on both like this one: |Balrog
rule|

Testing
~~~~~~~

You can use the nightlytest channel to test changes before sending them
to production. A widevine request to balrog is like this one:
https://aus5.mozilla.org/update/3/GMP/62.0/20180802174131/WINNT_x86_64-msvc-x64/en-US/nightlytest/default/default/default/update.xml

:warning:
  Reminder: In this URL, 62.0 can't be 62.0b14. Even though it
  works from Balrog's point of view, Firefox doesn't send this piece of
  data.

.. |Balrog rule| image:: /procedures/misc-operations/widevine-balrog-rule.png

