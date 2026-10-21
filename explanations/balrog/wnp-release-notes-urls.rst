WNP and Release Notes URL Configuration
========================================

The What's New Page (WNP) and release notes URLs that Balrog delivers to Firefox
clients are configured in ``browser/config/whats_new_page.yml`` in the Firefox
repository.

``whats_new_page.yml`` entry types
-----------------------------------

``product-details``
    Sets the ``detailsURL`` (release notes link, shown in About Firefox and the
    update prompt) for all channels.

``show-url``
    Sets the ``openURL`` (What's New Page shown after an update) conditionally
    per channel, locale list, and version range. Must include
    ``blob-types: [wnp]`` to ensure the entry only appears in the WNP blob.

URL placeholder resolution
---------------------------

- ``{product}``, ``{version}``, ``{version.major_number}``: resolved at task
  generation time by the ``release-balrog-submit-toplevel`` taskgraph transform.
- ``%LOCALE%``, ``%OLD_VERSION%``: resolved by Balrog at update delivery time.

Client-side release notes links
---------------------------------

The release notes links in the Firefox UI (About dialog, update prompt) are set
per-branding in ``browser/branding/*/pref/firefox-branding.js`` via:

- ``app.releaseNotesURL``
- ``app.releaseNotesURL.aboutDialog``
- ``app.releaseNotesURL.prompt``

The nightly fallback WNP URL is set via ``startup.homepage_override_url`` in
the nightly branding pref file.

Windows installer
------------------

``URLUpdateInfo`` in ``browser/branding/official/branding.nsi`` sets the
"Update information" URL written to the Windows registry uninstall key. Only
written for Release and ESR builds (not beta, nightly, or aurora).
