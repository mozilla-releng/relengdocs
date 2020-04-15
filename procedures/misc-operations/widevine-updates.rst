Widevine updates
================

Widevine is a system addon allowing Firefox user to read DRM'd content
(like Netflix). We provide updates via Balrog.

When
----

The request comes from the media team. They usually file a bug like
`this one. <https://bugzilla.mozilla.org/show_bug.cgi?id=1475260>`__

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
blob. The easiest way to do this is to download the most previous
release blob,
e.g.\ `Widevine-1.4.9.1088 <https://aus4-admin.mozilla.org/releases#Widevine-1.4.9.1088>`__.
Then open in an editor. It's small and should be like:

.. code:: json

   {
     "hashFunction": "sha512",
     "name": "Widevine-1.4.9.1088",
     "product": "Widevine",
     "schema_version": 1000,
     "vendors": {
       "gmp-widevinecdm": {
         "platforms": {
           "Darwin_x86_64-gcc3": {
             "alias": "Darwin_x86_64-gcc3-u-i386-x86_64"
           },
           "Darwin_x86_64-gcc3-u-i386-x86_64": {
             "fileUrl": "https://redirector.gvt1.com/edgedl/widevine-cdm/1.4.9.1088-mac-x64.zip",
             "filesize": 3220735,
             "hashValue": "79cde6f9457f1b46f03ba5baade0852ad2a7d640930c3229a750deb37b5061a9e75e8d6410a138bbdd7c871f8310476ad4a6f295cd05235ea9f392de339ff83c"
           },
           "Linux_x86-gcc3": {
             "fileUrl": "https://redirector.gvt1.com/edgedl/widevine-cdm/1.4.9.1088-linux-ia32.zip",
             "filesize": 3062013,
             "hashValue": "fb0207c6e24c05144ed345a6e37afc8e7bc2700c9bc4b536fa23503f08f2d258e10c4f1ef40f6ed0d6d8eaf495dbdcc924e71314cc1858f81fe6208cd210e8b5"
           },
           "Linux_x86_64-gcc3": {
             "fileUrl": "https://redirector.gvt1.com/edgedl/widevine-cdm/1.4.9.1088-linux-x64.zip",
             "filesize": 2921375,
             "hashValue": "8038d142f14b8992db282003ed7bd7fcb6a11c556fdfe34d410d017c3d8d792c24f38a24f6f65fea1a979a4c697f50cca826d8a28ae4fa9740512c3291d52aaf"
           },
           "Linux_x86_64-gcc3-asan": {
             "alias": "Linux_x86_64-gcc3"
           },
           "WINNT_x86-msvc": {
             "fileUrl": "https://redirector.gvt1.com/edgedl/widevine-cdm/1.4.9.1088-win-ia32.zip",
             "filesize": 3389392,
             "hashValue": "8e115f3f941663ac052570191acca09cb025388f82b232df5770aeb1781a611f002226de244ddd1b75553bbb5154068dca8913465b2c27ea28a1b4cae8359682"
           },
           "WINNT_x86-msvc-x64": {
             "alias": "WINNT_x86-msvc"
           },
           "WINNT_x86-msvc-x86": {
             "alias": "WINNT_x86-msvc"
           },
           "WINNT_x86_64-msvc": {
             "fileUrl": "https://redirector.gvt1.com/edgedl/widevine-cdm/1.4.9.1088-win-x64.zip",
             "filesize": 3351002,
             "hashValue": "48b25b1a89ac07fa041c17ff4ae6ac43171a69a7fdcb226c09150b8ecc824dc3a7fa2f2a9f607c35fb5e1e234cfc0bd717a9a48883fc8084ac0743f2e695bbf8"
           },
           "WINNT_x86_64-msvc-x64": {
             "alias": "WINNT_x86_64-msvc"
           }
         },
         "version": "1.4.9.1088"
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

