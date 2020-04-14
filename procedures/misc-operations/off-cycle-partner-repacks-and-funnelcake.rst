Original docs are
`here <https://mana.mozilla.org/wiki/display/RelEng/Partner+Repack+Creation>`__.

Background
==========

We repackage Firefox for partners. Occasionally we’ll have a new study
(funnelcake) or a new partner or partner config that happens after a
release is built, but before the next release is scheduled to be built,
and we need to repack that partner off-cycle.

When?
=====

We’ll get a bug for a new partner repack or funnelcake, in the Release
Engineering :: Custom Release Requests component in Bugzilla.

These will need to run against a previously-promoted release.

**Warning:** Adding a new partner, or partner sub-config, can cause
alarming failures for an in-progress Firefox release, but does not
actually block the release. The problem usually occurs in the push or
ship phase, where a new partner config since the previous phase causes
extra partner tasks in the new graph and these fail. A resolution for
this is tracked in `Bug
1496530 <https://bugzilla.mozilla.org/show_bug.cgi?id=1496530>`__, but
in the meantime you can either delay the partner configuration change
until the release is complete, or inform releaseduty to ignore the extra
tasks.

How?
====

These are the steps on how to trigger the
repack/signing/repackage/repackage-signing/beetmover tasks for partner
repacks and funnelcakes. We sometimes still have additional steps
afterwards, until we automate everything.

Preparation
-----------

1. Clone `braindump <https://hg.mozilla.org/build/braindump/>`__ and set
   up a virtualenv with requests and pyyaml.
   ``hg clone https://hg.mozilla.org/build/braindump/     cd braindump/releases-related     python3 -m venv ./venv     . venv/bin/activate     pip install requests pyyaml``
   or update your existing clone.

2. Determine the version and build number we’re going to use. This is
   generally the most recent Firefox release, but might be ESR or beta.

3. Determine the partner name - this will be usually be given in the
   bug. There should be a repo at
   ``https://github.com/mozilla-partners/<name>/`` - you may have to
   figure out the parent of a sub-config.

   Until `Bug
   1530231 <https://bugzilla.mozilla.org/show_bug.cgi?id=1530231>`__ is
   resolved we support a single, top-level config, eg ``funnelcake``,
   but not ``funnelcakeNNN`` or ``yandex,ironsource``. If more than one
   partner is needed create separate graphs using separate custom
   actions.

4. Generate the action input, eg
   ``./off-cycle-parter-respin.py -v 65.0.2 -b release -p seznam``

5. Load the Treeherder link given near the bottom of the output. Make
   sure you are logged into Treeherder. In the top-right corner of the
   UI for the push locate the small triangle, select
   ``Custom Push Action...`` from the dropdown list.

6. From the ``Action`` dropdown select ``Release Promotion``.

7. Paste action input the script has generated into the ``Payload`` box,
   click the ``Trigger`` button.

8. Treeherder will display a link to the Taskcluster task for a few
   seconds, otherwise look for the ``firefox_promote_partners`` job in
   the ``Gecko Decision Task`` line. The graphs are small enough they
   can be monitored in a browser tab, but you can also use
   ``braindump//taskcluster/graph-progress.sh``.

9. When the graph is done, resolve the bug. If there are tasks in the
   graph matching ``release-partner-repack-beetmover-*-public``, add the
   link to the candidates directory which the
   ``off-cycle-parter-respin.py`` script provides; otherwise the repacks
   will be available in the partners portal.

Additional steps
----------------

Funnelcake
~~~~~~~~~~

For funnelcake, we still need to deal with bouncer. See the
bouncer-related docs
`here <https://mana.mozilla.org/wiki/display/RelEng/Partner+Repack+Creation#PartnerRepackCreation-Funnelcakebuilds>`__.

Stub installers
~~~~~~~~~~~~~~~

We have some manual steps to copy files and set up bouncer for stub
installers, as this is not automated in the respin case. Regular
releases do not require this work, and automating respins is covered by
`Bug 1583685 <https://bugzilla.mozilla.org/show_bug.cgi?id=1583685>`__.

1. First, define some parameters. You can most of this from the output
   of the script, but ``PARTNER_SUB_CONFIGS`` will depend on which
   sub-configs are of interest in this respin. eg:
   ``VERSION=69.0.1     BUILDN=build1     PARTNER=softonic     PARTNER_SUB_CONFIGS="softonic-010 softonic-011 softonic-012"     PARTNER_BUILDN=v201909242143``

2. To push the files into ``firefox/releases/partners`` you’ll need a
   copy of the ``release`` beetmover credentials in your
   ``~/.aws/credentials``, in the ``[temp]`` section. Then
   ``# you can echo the commands or add the --dryrun argument to test this     for P_SUB in ${PARTNER_SUB_CONFIGS}; do         AWS_PROFILE=temp aws s3 sync \           s3://net-mozaws-prod-delivery-firefox/pub/firefox/candidates/${VERSION}-candidates/${BUILDN}/partner-repacks/${PARTNER}/${P_SUB}/${PARTNER_BUILDN}/ \           s3://net-mozaws-prod-delivery-firefox/pub/firefox/releases/partners/${PARTNER}/${P_SUB}/${VERSION}/     done``
   Clean up the credentials immediately after use!

3. To set up the bouncer products, locations, and aliases, generate the
   config with \``\` for P_SUB in
   :math:`{PARTNER_SUB_CONFIGS}; do  ## add products  echo "new product: Firefox-`\ {VERSION}-:math:`{PARTNER}-`\ {P_SUB}
   with SSL disabled, locales not set" echo “new location: win :
   /firefox/releases/partners/:math:`{PARTNER}/`\ {P_SUB}/:math:`{VERSION}/win32/:lang/Firefox%20Setup%20`\ {VERSION}.exe”
   echo “new location: win64 :
   /firefox/releases/partners/:math:`{PARTNER}/`\ {P_SUB}/:math:`{VERSION}/win64/:lang/Firefox%20Setup%20`\ {VERSION}.exe”
   echo “new location: osx :
   /firefox/releases/partners/:math:`{PARTNER}/`\ {P_SUB}/:math:`{VERSION}/mac/:lang/Firefox%20`\ {VERSION}.dmg”

   echo “new product:
   Firefox-:math:`{VERSION}-`\ {PARTNER}-:math:`{P_SUB}-stub with SSL enabled"  echo "new location: win and win64: /firefox/releases/partners/`\ {PARTNER}/:math:`{P_SUB}/`\ {VERSION}/win32/:lang/Firefox%20Installer.exe”

   ## add aliases echo “new alias:
   partner-firefox-release-:math:`{PARTNER}-`\ {P_SUB}-latest –>
   Firefox-:math:`{VERSION}-`\ {PARTNER}-:math:`{P_SUB}"  echo "new alias: partner-firefox-release-`\ {PARTNER}-:math:`{P_SUB}-stub --> Firefox-`\ {VERSION}-:math:`{PARTNER}-`\ {P_SUB}-stub”
   echo done \``\` then go to
   `Bounceradmin <https://bounceradmin.mozilla.com/admin/>`__ to add
   entries listed, with the usual `tunnel to gain
   access <https://github.com/mozilla-releng/releasewarrior-2.0/blob/master/docs/misc-operations/accessing-bouncer.md>`__.
   This work will need to be scripted once we move to Nazgul and only
   have an HTTP API to work with.

4. Verify that redirects from bouncer end up on the expected files:
   ``for P_SUB in ${PARTNER_SUB_CONFIGS}; do       echo '------------------------------------------------------------------------';       echo Checking ${PARTNER} ${P_SUB} full installer       for os in {win64,win,osx}; do         url="https://download.mozilla.org/?product=partner-firefox-release-${PARTNER}-${P_SUB}-latest&os=${os}&lang=en-US";         echo $url;         curl -sIL $url | egrep "^HTTP|^Location";         echo;       done;       echo Checking ${PARTNER} ${P_SUB} stub installer       for os in {win64,win}; do         url="https://download.mozilla.org/?product=partner-firefox-release-${PARTNER}-${P_SUB}-stub&os=${os}&lang=en-US";         echo $url;         curl -sIL $url | egrep "^HTTP|^Location";         echo;       done;     done``
   You should see output like this, indicating a 302 from bouncer to the
   CDN, with a 200 response from there:
   ``Checking softonic softonic-010 full installer     https://download.mozilla.org/?product=partner-firefox-release-softonic-softonic-010-latest&os=win64&lang=en-US     HTTP/1.1 302 Found     Location: https://download-installer.cdn.mozilla.net/pub/firefox/releases/partners/softonic/softonic-010/69.0.1/win64/en-US/Firefox%20Setup%2069.0.1.exe     HTTP/2 200    ...``

Future
======

In the future, we can use `action
hooks <https://bugzilla.mozilla.org/show_bug.cgi?id=1415868>`__ for
this. In addition, we can do things like add bouncer tasks in a shipping
phase that allow us to automate the final remaining manual steps.

Ideally, ship-it v2 will be the forward-facing UI instead of hooks or an
ssh shell. This is tracked in `bug
1530859 <https://bugzilla.mozilla.org/show_bug.cgi?id=1530859>`__.
