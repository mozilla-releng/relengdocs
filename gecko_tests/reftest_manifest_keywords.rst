.. _mochitest_xpcshell_manifest_keywords:

Adding a keyword to reftest style manifests
====================================================

Reftests use a series of runtime and build properties to skip or allow for pixels to not match.

Current behavior
----------------

Currently, gecko builds generate a ``target.mozinfo.json`` with metadata about the build. An example ``target.mozinfo.json`` might look like :download:`this <target.mozinfo.json>`. This is consumed in the reftest harness and translated into keywords that reftest uses::

    fuzzyIf(cocoaWidget&&isDebugBuild,1-1,85-88)

In this case, ``cocoaWidget`` and ``isDebugbuild`` are keywords (that are defined in the reftest harness). Keywords are essentially booleans in mozinfo, since we don't have to compare them to something like ``os == 'win'``.

The test will download the build's ``target.mozinfo.json``, then in addition to the mozinfo, will query runtime info from the browser to build a sandbox of keywords. This logic lives in `manifest.jsm <https://searchfox.org/mozilla-central/source/layout/tools/reftest/manifest.jsm#439>`__.

How to add a keyword
--------------------

For manifestparser, we add info to mozinfo, but for reftest, we need to add it to the sandbox.  For example, for Apple Silicon, we can add an ``apple_silicon`` keyword with a patch like this:

.. code-block:: diff

    --- a/layout/tools/reftest/manifest.jsm
    +++ b/layout/tools/reftest/manifest.jsm
    @@ -572,16 +572,18 @@ function BuildConditionSandbox(aURL) {
    
        // Set OSX to be the Mac OS X version, as an integer, or undefined
        // for other platforms.  The integer is formed by 100 times the
        // major version plus the minor version, so 1006 for 10.6, 1010 for
        // 10.10, etc.
        var osxmatch = /Mac OS X (\d+).(\d+)$/.exec(hh.oscpu);
        sandbox.OSX = osxmatch ? parseInt(osxmatch[1]) * 100 + parseInt(osxmatch[2]) : undefined;
    
    +    sandbox.apple_silicon = sandbox.cocoaWidget && sandbox.OSX>=11;
    +
        // Plugins are no longer supported.  Don't try to use TestPlugin.
        sandbox.haveTestPlugin = false;
    
        // Set a flag on sandbox if the windows default theme is active
        sandbox.windowsDefaultTheme = g.containingWindow.matchMedia("(-moz-windows-default-theme)").matches;
    
        try {
            sandbox.nativeThemePref = !prefs.getBoolPref("widget.disable-native-theme-for-content");


To use this, you would just edit a manifest similar to this:

.. code-block:: diff

    --- a/layout/reftests/table-bordercollapse/reftest.list
    +++ b/layout/reftests/table-bordercollapse/reftest.list
    @@ -29,58 +29,58 @@ random-if(/^Windows\x20NT\x206\.1/.test(
    == bc_dyn_table1.html bc_dyn_table1_ref.html
    == bc_dyn_table2.html bc_dyn_table2_ref.html
    == bc_dyn_table3.html bc_dyn_table3_ref.html
    == bc_borderoffset1.html bc_borderoffset1_ref.html
    == bc_borderoffset2.html bc_borderoffset2_ref.html
    == frame_above_rules_all.html frame_above_rules_all_ref.html
    == frame_above_rules_cols.html frame_above_rules_cols_ref.html
    == frame_above_rules_groups.html frame_above_rules_groups_ref.html
    -== frame_above_rules_none.html frame_above_rules_none_ref.html
    +fuzzy-if(apple_silicon,1-1,281-281) == frame_above_rules_none.html frame_above_rules_none_ref.html
    == frame_above_rules_rows.html frame_above_rules_rows_ref.html
    == frame_below_rules_all.html frame_below_rules_all_ref.html
    == frame_below_rules_cols.html frame_below_rules_cols_ref.html
    == frame_below_rules_groups.html frame_below_rules_groups_ref.html
 