How to automate nightly Google Play deployments
===============================================

These instructions define how to set up an Android product for nightly
deployments to the Google Play store.

Throughout this document, wherever the term ``$product`` is used,
substitute your product's name in (replacing spaces with hyphens), e.g.:
``reference-browser`` or ``fenix``.

Ideally, we shouldn't use the below docs, but instead use pushapk in taskgraph.

Note: we don't need to explicitly "create" scopes in Taskcluster. We'll
simply tell Taskcluster that our hook *has* some scopes, then later
we'll tell it that we'll need those scopes to run our builds.
Taskcluster will just verify that the scopes we're using dynamically
match between the build and the hook that starts the build.

1.  Request signing keys (example bug for
    `reference-browser <https://bugzilla.mozilla.org/show_bug.cgi?id=1508761>`__).
    Confirm with the app's team what the "signature algorithm" and
    "digest algorithm" should be, and include that information in the
    ticket.

    -  You'll want at least one "dep" key for testing, as well as a
       separate "release" key for every separate app that will be
       created (e.g.: ``nightly``, ``beta`` and ``production``)

2.  Clone the product's repository

3.  Add ``.taskcluster.yml`` in the root of the repository. This file
    tells Taskcluster what to do upon github events happening (push,
    pr, release, etc). Since we're going to want to run ``taskgraph``
    to decide what tasks to run, we can take a ``.taskcluster.yml`` from
    a similarly-configured repository, like `fenix
    example <https://github.com/mozilla-mobile/fenix/blob/master/.taskcluster.yml>`__)

    -  Update repository and treeherder references to refer to your project,
       rather than ``fenix``.

4.  Implement ``taskgraph`` configuration for the repository. See the
    `Fenix configuration <https://github.com/mozilla-mobile/fenix/tree/master/taskcluster>`__.
    You'll need to implement the following parts:

    -  Define tasks in YAML in ``taskcluster/ci/``
    -  Define transforms in ``taskcluster/$project_taskgraph/transforms/`` which operate
       on the tasks defined in the YAML
    -  Define any custom loaders in ``taskcluster/$project_taskgraph/loader/`` (this is
       useful in cases like needing to generate a dynamic number of tasks based on an
       external source, like ``gradle`` or a ``.buildconfig.yml`` file)
    -  Define ``Dockerfiles`` in ``taskcluster/docker/``

5.  Create and update permissions in ``ci-configuration``.

    1. Install ``ci-admin`` if you haven't already

        1. ``hg clone https://hg.mozilla.org/ci/ci-admin/``
        2. Set up a ``virtualenv`` and install dependencies

    1. ``hg clone https://hg.mozilla.org/ci/ci-configuration/``
    2. Update ``projects.yml`` and ``grants.yml`` to add permissions for ``$project``

        - If you have schedule-based automation, add the ``taskgraph-cron`` feature and set ``cron_targets`` in ``projects.yml``. Additionally, create
          a ``.cron.yml`` file to your repository like the one in `fenix <https://github.com/mozilla-mobile/fenix/blob/master/.cron.yml>`__
    3. Submit your patch for review with `moz-phab <https://github.com/mozilla-conduit/review>`__
    4. Once it's landed, update to the new revision and apply it

        1. ``ci-admin diff --environment=production``
        2. If there's no surprises in the diff, apply it: ``ci-admin apply --environment=production``
        3. If the diff contains changes other than the hooks and permissions you added, you can adjust the ``diff``
           and ``apply`` operations with the ``--grep`` flag:

            ``ci-admin diff --environment=production --grep "AwsProvisionerWorkerType=mobile-\d-b-firefox-tv"``

6.  Update ``scriptworker`` (`example for
    ``fenix`` <https://github.com/mozilla-releng/scriptworker/pull/298>`__)

    1. Update ``scriptworker/constants.py`` with entries for your product. Search for
       locations where "fenix" or "firefox-tv" were set up, and add your product accordingly
    2. In a separate commit, bump the minor version and add a changelog
       entry
       (`example <https://github.com/mozilla-releng/scriptworker/commit/55626556eaf3aebdcf6aba408757bc39b76a941a>`__)
    3. Once these changes are CR'd and merged, publish the new version

       1. Update your repository against the ``mozilla-releng``
          repository
       2. Check out the version-bump commit you created
       3. ``git tag $version``, e.g.: ``git tag 23.3.1``
       4. ``git push --tags && git push upstream --tags`` (assuming that
          the ``origin`` remote is for your fork, and ``upstream`` is
          the ``mozilla-releng`` repo)
       5. Ensure you're in the Python virtual env for your package (One
          approach is to share a single virtual env between all
          scriptworker repos)
       6. ``rm -rf dist && python setup.py sdist bdist_wheel`` build the
          package
       7. Publish to PyPI:

          1. ``gpg --list-secret-keys --keyid-format long`` to get your
             GPG identity (it's the bit after "sec rsaxxxx/"). An
             example GPG identity would be ``5F2B4756ED873D23``
          2. ``twine upload --sign --identity $identity dist/*`` to
             upload to Pypi (you may need to ``pip install twine``
             first)

7. Update configuration in
    `scriptworker-scripts <https://github.com/mozilla-releng/scriptworker-scripts/>`__

    1. Locate signing secrets (dep signing username and password, prod
       signing username and password, Google Play service account and
       password)

       1. You should've received signing credentials from step 1. Print
          out the decrypted file you received:
          ``gpg -d <file from step 1>``
       2. We will want to encrypt the "dep" and "rel" credentials for
          the "prod" autograph instance. They can be identified as lines
          that contain a "list" where the second item ends with "_dep"
          or "_prod", respectively

          -  Example: "dep" line would be:
             ``["http://<snip>", "signingscript_fenix_dep", "<snip>", ["autograph_apk"], "autograph"]``

       3. For these two lines, the secrets we want to put in sops are
          the username and password (the second and third item)
       4. Later, in step 18, you'll have been emailed a Google Play
          service account and key. However, for now, we're going to use
          a dummy value (the string "dummy") as placeholders for these
          values

    2. Add secrets to ``SOPS``

       1. TODO

8. Commit and push your ``SOPS`` and scriptworker-scripts changes, make a PR

9. Once step 8's PR is approved, merge the ``scriptworker-scripts`` PR

10. Verify with app's team how ``versionCode`` should be set up. Perhaps
    by date like
    `fenix <https://github.com/mozilla-mobile/fenix/blob/master/automation/gradle/versionCode.gradle>`__?

    -  Note that if there's multiple build types, they need different
       version codes. In the case of
       `fenix <https://github.com/mozilla-mobile/fenix/blob/master/app/build.gradle#L50-L52>`__,
       ``x86`` builds have the version code incremented by 1.

11. When the Google Play product is being set up, an officially-signed
    build with a version code of 1 needs to be built. So, the main
    automation PR for the product will need to be stunted: it needs to
    produce APKs with a version code of 1, and it should have pushing to
    Google Play disabled (so we don't accidentally push a build before
    our official version-code-1 build is set up).

    1. Change the version code to be set to 1. If the product uses the
       same version-code-by-date schema as ``fenix``, then edit
       `versionCode.gradle <https://github.com/mozilla-mobile/fenix/pull/156/files#diff-63606bb315fadc051f73a54767849985R41>`__
    2. `Disable the creation of the task that pushes to Google
       Play <https://github.com/mozilla-mobile/fenix/pull/156/files#diff-73e51d972c105de5122ec559909980daR123>`__
    3. Create the PR
    4. Once approved, merge the PR

12. Verify the apk artifact(s) of the signing task

    1. Trigger the nightly hook
    2. Once the build finishes, download the apks from the signing task
    3. Using the prod certificate from step 10.iv.a., create a temporary
       keystore:
       ``keytool -import -noprompt -keystore tmp_keystore -storepass 12345678 -file $product_release.pem -alias $product-rel``
    4. For each apk, verify that it matches the certificate:
       ``jarsigner -verify $apk -verbose -strict -keystore tmp_keystore``.
       Check that

       -  The "Digest algorithm" matches step 1
       -  The "Signature algorithm" matches step 1
       -  There are no warnings that there are entries "whose
          certificate chain invalid", "that are not signed by alias in
          this keystore" or "whose signer certificate is self-signed"

    -  Do the same thing for the dep signing task and certificate and
       check that the ``jarsigner`` command shows that the "Signed by"
       ``CN`` is "Throwaway Key"

13. Request both the creation of a Google Play product and for the
    credentials to publish to it. Consult with the product team to `fill
    out the requirements for adding an app to Google
    Play <https://wiki.mozilla.org/Release_Management/Adding_a_new_app_on_Google_play>`__.
    This request should be a bug for "Release Engineering > Release
    Automation: Pushapk", and should be a combination of
    `this <https://bugzilla.mozilla.org/show_bug.cgi?id=1508294>`__ and
    `this <https://bugzilla.mozilla.org/show_bug.cgi?id=1512173>`__

    -  As part of the bug, note that you'll directly send an APK to the
       release management point of contact via Slack

14. Give the first signed APK to the Google Play admins

    1. Perform a nightly build
    2. Once the signing task is done, grab the APK with the version code
       of 1 (if there's multiple APKs, you probably want the arm one)

       -  You can verify the version code of the apk with
          `apktool <https://ibotpeaches.github.io/Apktool/>`__, then
          viewing the extracted ``AndroidManifest.xml`` and looking at
          the ``platformBuildVersionCode``

    3. Send the APK to release management

15. Once the previous step is done and they've set up a Google Play
    product, put the associated secrets in SOPS

16. Perform a new PR that un-stunts the changes from step 15 `Fenix
    example <https://github.com/mozilla-mobile/fenix/pull/161>`__

    -  Version code should be generated according to how the team
       requested in step 14
    -  The task that pushes to Google Play should no longer be disabled

17. Once the PR from the last step is merged, trigger the nightly task, verify
    that it uploads to Google Play

18. Update the ``$product-nightly`` hook, adding a schedule of
    ``0 12 * * *`` (make it fire daily)

    -  Ensure that the hook is triggered automatically by waiting a day,
       then checking the hook or indexes

How to test release graphs in mobile
====================================

Use the `staging android-components <https://github.com/mozilla-releng/staging-android-components>`__ and `staging fenix <https://github.com/mozilla-releng/staging-fenix>`__ repos, along with `staging shipit <https://shipit.staging.mozilla-releng.net/>`__.

How to set up taskgraph for mobile
==================================

Setting up taskgraph for mobile is similar to setting up taskgraph for any
standalone project, especially github standalone projects: install
`taskgraph <https://hg.mozilla.org/ci/taskgraph>`__ in a virtualenv.

⚠️ You shouldn't install ``gradle`` globally on your system. The `./gradlew` scripts in each mobile repo define
specific gradle versions and are in charge of installing it locally.

1. Install jdk8::

    # On mac with homebrew
    brew install --cask homebrew/cask-versions/adoptopenjdk8

    # On Ubuntu
    sudo apt install openjdk-8-jdk

⚠️ Currently projects like Focus and Fenix need Java 11 to run, so you might need to install that version and set your $JAVA_HOME to that version.

2. Install android-sdk::

    # On mac with homebrew
    brew install --cask android-sdk

    # On Ubuntu
    sudo apt install android-sdk

3. Make sure you're pointing to the right java (depending on what version gradle requires)::

    # In your .zshrc or .bashrc:
    # On mac
    export JAVA_HOME="$(/usr/libexec/java_home -v 1.8)"

    # On Ubuntu follow symlinks to find JAVA_HOME
    ls -l `which java`
    export JAVA_HOME=<JAVA_HOME>

    # After sourcing that file, you should get the following version:
    # > $JAVA_HOME/bin/java -version
    # openjdk version "1.8.0_265"
    # OpenJDK Runtime Environment (AdoptOpenJDK)(build 1.8.0_265-b01)
    # OpenJDK 64-Bit Server VM (AdoptOpenJDK)(build 25.265-b01, mixed mode)

4. You'll also need to setup ``ANDROID_SDK_ROOT``::

    # In your .zshrc or .bashrc:
    # On mac
    export ANDROID_SDK_ROOT=/usr/local/Caskroom/android-sdk/4333796

    # On Ubuntu
    export ANDROID_SDK_ROOT=/usr/lib/android-sdk
    
    # For Ubuntu, you'll also need to grab the Android cmdline-tools (which contains sdkmanager).
    # First download the linux 'cmdline-tools' from here: https://developer.android.com/studio/index.html#downloads
    # Then:
    mkdir $ANDROID_SDK_ROOT/cmdline-tools
    unzip <commandlinetools.zip> -d $ANDROID_SDK_ROOT/cmdline-tools/latest
    export PATH=$ANDROID_SDK_ROOT/cmdline-tools/latest/bin:$PATH
    
    # Verify the `sdkmanager` binary is available:
    which sdkmanager

5. You'll need to accept all licenses before you can build the app::

    # on mac
    cd /usr/local/Caskroom/android-sdk/4333796
    yes | sdkmanager --licenses

   ⚠️ If you hit this error: ``Exception in thread "main" java.lang.NoClassDefFoundError: javax/xml/bind/annotation/XmlSchema``
   you might need to either switch to java8 to accept the licenses and if that doesn't work then run::
   
    yes | sdkmanager --update 
    # to accept licenses for the sdkmanager itself

    yes | sdkmanager --licenses 
    # to accept new licenses not previously accepted

   Additional troubleshooting tips can be found on `this stack overflow thread <https://stackoverflow.com/questions/38096225/automatically-accept-all-sdk-licences>`

6. Test it::

    # In, say, an android-components or fenix clone, this should work:
    ./gradlew tasks --scan

7. You'll need a Python 3 virtualenv with taskgraph, glean-parser, and mozilla-version as well::

    virtualenv fenix  # or whatever the repo name
    pushd ../taskgraph  # assuming taskgraph is cloned in the same dir
    python setup.py install
    popd
    pip install mozilla-version glean-parser<1

    # Verify taskgraph optimized returns tasks (You need https://hg.mozilla.org/build/braindump/ cloned)
    # android-components
    taskgraph optimized -p ../braindump/taskcluster/taskgraph-diff/params-android-components/main-repo-release.yml

    # fenix
    taskgraph optimized -p ../braindump/taskcluster/taskgraph-diff/params-fenix/main-repo-push.yml


8. To run ``taskgraph-gen.py``::

    # set $TGDIR to the braindump/taskcluster directory path
    TGDIR=..

    # Fenix
    $TGDIR/taskgraph-diff/taskgraph-gen.py --halt-on-failure --overwrite --params-dir $TGDIR/taskgraph-diff/params-fenix --full fenix-clean 2>&1 | tee out

    # Android-Components
    $TGDIR/taskgraph-diff/taskgraph-gen.py --halt-on-failure --overwrite --params-dir $TGDIR/taskgraph-diff/params-android-components --full ac-clean 2>&1 | tee out

9. To test taskgraph changes without braindump, run `taskgraph target-graph -p parameters.yml`. But you might need to go into an existing task in taskcluster and download a parameters artifact.
