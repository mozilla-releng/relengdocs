.. _mochitest_xpcshell_manifest_keywords:

Adding a keyword to mochitest and xpcshell manifests
====================================================

Keywords in mochitest and xpcshell test manifests allow us to determine which tests we want to skip and which we want to run.

Current behavior
----------------

Currently, gecko builds generate a ``target.mozinfo.json`` with metadata about the build. An example ``target.mozinfo.json`` might look like :download:`this <target.mozinfo.json>`. This lets us use ``skip-if`` in test manifests, like::

    skip-if = e10s && os == 'win'

In this case, ``e10s`` is a keyword. Keywords are essentially booleans in mozinfo, since we don't have to compare them to something like ``os == 'win'``.

The test will download the build's ``target.mozinfo.json``, then update the mozinfo dictionary with additional runtime information based on the task or runtime environment. This logic lives in `mozinfo <https://hg.mozilla.org/mozilla-central/file/default/testing/mozbase/mozinfo/mozinfo/mozinfo.py>`__.

How to add a keyword
--------------------

The easiest route may be to patch mozinfo. For example, for Apple Silicon, we can add an ``apple_silicon`` keyword with a patch like this:

.. code-block:: diff

    --- a/testing/mozbase/mozinfo/mozinfo/mozinfo.py
    +++ b/testing/mozbase/mozinfo/mozinfo/mozinfo.py
    @@ -144,19 +144,29 @@ elif system == "Darwin":
         os_version = "%s.%s" % (versionNums[0], versionNums[1])
         info["os"] = "mac"
     elif sys.platform in ("solaris", "sunos5"):
         info["os"] = "unix"
         os_version = version = sys.platform
     else:
         os_version = version = unknown
     
    +info["apple_silicon"] = False
    +if (
    +    info["os"] == "mac"
    +    and float(os_version) > 10.15
    +    and processor == "i386"
    +    and bits == "64bit"
    +):
    +    info["apple_silicon"] = True
    +
     info["version"] = version
     info["os_version"] = StringVersion(os_version)
     
    +
     # processor type and bits
     if processor in ["i386", "i686"]:
         if bits == "32bit":
             processor = "x86"
         elif bits == "64bit":
             processor = "x86_64"
     elif processor.upper() == "AMD64":
         bits = "64bit"
