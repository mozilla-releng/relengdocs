Desktop Flatpak Releases
========================

Flatpak is a package format that targets to support every Linux
distribution. We’ve made Firefox publicly available on
https://flathub.org/apps/details/org.mozilla.firefox since Firefox 74.0.

Channels used
-------------

As of September, 2020 we build and publish two flatpaks: \* mozilla-beta
flatpak that is published to the Flathub ``beta`` channel. This does not
have an UI and is used by ~1K users. It’s mainly for testing purposes \*
mozilla-release flatpak that is published to the Flathub ``stable``
channel[2]. This is the main flatpak that users get.

In order to publish to both channels, we use the flatpak
scriptworker[3]. The procedure to push is the same for both channels,
only the ``token`` value depends. Both of them are baked in our SOPS.

The flatpak store (Flathub) comes with the concept of tracks (à la
Google Play Store). Release promotion automatically uploads to these
tracks:

+---------------------------+------------+---------------------------+
| Brand name                | Track      | Notes                     |
+===========================+============+===========================+
| Firefox                   | ``stable`` | Automatically shipped     |
|                           |            | from ``mozilla-release``  |
+---------------------------+------------+---------------------------+
| Firefox beta              | ``beta``   | Automatically shipped     |
|                           |            | from ``mozilla-beta``     |
+---------------------------+------------+---------------------------+
| Firefox Developer Edition | N/A        | Not supported yet         |
+---------------------------+------------+---------------------------+
| Firefox Nightly           | N/A        | Not supported yet         |
+---------------------------+------------+---------------------------+
| Firefox ESR               | N/A        | Not supported yet         |
+---------------------------+------------+---------------------------+

Changes to Flatpak via web interface
------------------------------------

As of September 2020, the Flatpak doesn’t have a formal UI to make
changes to the flatpaks via authorized credentials. Most of the
applications shipped to Flathub are done so as part of the Flathub’s CI
on Github. Firefox is among the very few applications that are being
shipped directly from our automation via Flathub’s API.

For any urgent changes, Flathub administrators have leverage and can be
contacted to help. Details on how to contact them ca be found in the
private repo within the ``flathub-store.txt`` file.

## Refresh Flathub credentials
------------------------------

In order to publish to both channels, we use the flatpak
`scriptworker`_. The procedure to push is the same for both channels,
only the ``token`` value depends. When these tokens expiry, they need to
be refreshed. Specific instructions on how to do that lie within the
``flathub-store.txt`` in the private repo.

.. _scriptworker: https://github.com/mozilla-releng/scriptworker-scripts/tree/master/pushflatpakscript
