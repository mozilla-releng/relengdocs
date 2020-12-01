How to automate nightly Google Play deployments
===============================================

These instructions define how to set up an Android product for nightly
deployments to the Google Play store.

Throughout this document, wherever the term ``$product`` is used,
substitute your product's name in (replacing spaces with hyphens), e.g.:
``reference-browser`` or ``fenix``.

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
    `build-puppet <https://github.com/mozilla-releng/build-puppet/>`__

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

       3. For these two lines, the secrets we want to put in hiera are
          the username and password (the second and third item)
       4. Later, in step 18, you'll have been emailed a Google Play
          service account and key. However, for now, we're going to use
          a dummy value (the string "dummy") as placeholders for these
          values

    2. Add secrets to ``hiera``

       1. Connect to VPN
       2. SSH into ``releng-puppet2.srv.releng.mdc1.mozilla.com``
       3. ``sudo cp /etc/hiera/secrets.eyaml /etc/hiera/secrets.eyaml.$username-$date``
          (substituting in your username and the date in the format
          ``YYYYMMDD``, like ``20181231``) to back up the hiera secrets
          file
       4. For each secret, `encrypt
          it <https://wiki.mozilla.org/ReleaseEngineering/PuppetAgain/Secrets#Using_EYAML>`__
          with
          ``sudo eyaml encrypt --pkcs7-private-key /etc/hiera/keys/private_key.pem --pkcs7-public-key /etc/hiera/keys/public_key.pem --output examples -p -l '$lookupkey'``
          (it prompts you to paste the secret). The "lookup key" is
          different for each secret we put in Hiera:

          -  The autograph username's lookup key will be:
             ``autograph_$product_$level_username`` (e.g.:
             ``autograph_fenix_dep_username`` or
             ``autograph_fenix_prod_username``)
          -  The autograph password's lookup key will be
             ``autograph_$product_$level_password`` (e.g.:
             ``autograph_fenix_prod_password``)

             -  Note that "autograph" uses the term "rel" when we use
                the term "prod" - make sure the lookup key of your
                secrets uses our terminology of "prod"!

          -  The google service account's lookup key is
             ``service_account``
          -  The google play p12 file's lookup key is ``certificate``

       5. ``sudo vi /etc/hiera/secrets.eyaml``
       6. Look for the equivalent ``fenix`` secrets (Use the ``/`` to
          search, then type "fenix", then "enter", hitting ``n`` each
          time you want to step forward) and place your new products
          secrets in the same way

          -  For the two Google Play credentials, you may need to paste
             the encrypted secret in an IDE and space-indent it to the
             same level so it matches the indentation of the other
             Google Play credentials in the file

       7. Save (``:x``, enter) to save the file
       8. Disconnect from the puppet master

    3. In ``modules/signing_scriptworker``

       1. You should've received signing credentials from step 1. Print
          out the decrypted file you received:
          ``gpg -d <file from step 1>``
       2. With the output, find the "prod creds" section, and copy the
          line where the second array item ends in "_dep" (this is the
          dep autograph config)
       3. Edit ``templates/dep-passwords-mobile.json.erb``. Add a new
          scope section in the format
          ``project:mobile:$product:releng:signing:cert:dep-signing``

          1. Paste the dep autograph config (remove the trailing comma,
             if any)
          2. Replace the second item in that list you pasted so that,
             instead of having the autograph username, it has
             ``<%= scope.function_secret(["autograph_$product_dep_username"]) %>``
             (so it fetches from ``hiera``)
          3. Replace the third item in that list you pasted so that,
             instead of having the autograph password, it has
             ``<%= scope.function_secret(["autograph_$product_dep_password"]) %>``
             (so it fetches from ``hiera``)

       4. Edit ``templates/passwords-mobile.json.erb``. Add a new scope
          section in the format
          ``project:mobile:$product:releng:signing:cert:release-signing``

          1. Paste the prod autograph config (remove the trailing comma,
             if any)
          2. Replace the second item in that list you pasted so that,
             instead of having the autograph username, it has
             ``<%= scope.function_secret(["autograph_$product_prod_username"]) %>``
             (so it fetches from ``hiera``)
          3. Replace the third item in that list you pasted so that,
             instead of having the autograph password, it has
             ``<%= scope.function_secret(["autograph_$product_prod_password"]) %>``
             (so it fetches from ``hiera``)

       5. Edit ``manifests/settings.pp``, adding the new scope prefix
          ``project:mobile:$product:releng:signing:`` to the
          ``scope_prefixes`` property of both ``mobile-dep`` and
          ``mobile-prod``
       6. In ``files/requirements.txt``

          1. From step 9, update the version of ``scriptworker``

    4. In ``modules/pushapk_scriptworker``

       1. From step 1, you should have received two certificates (one
          for dep, and one for prod). They start with
          ``---BEGIN CERTIFICATE---`` and end with
          ``---END CERTIFICATE---``, and were probably sent in the
          gpg-encrypted text file with the autograph credentials. For
          each of these, copy them, remove any indentation they may
          have, and put them both in the ``files`` directory of
          ``pushapk_scriptworker`` with the names ``$product_dep.pem``
          and ``$product_release.pem``
       2. In ``manifests/settings.pp``

          1. In ``$_env_configs`` for ``mobile-dep`` and
             ``mobile-prod``, add the new scope prefix
             ``project:mobile:$product:releng:googleplay:product:`` to
             the ``scope_prefixes`` property
          2. In ``$pushapk_scriptworker_env`` for ``mobile-dep``, add a
             dictionary to ``$product_config`` such that:

             -  The ``product_names`` list includes ``$product``
             -  ``package_names`` includes your app's package name
             -  ``service_account`` set to "dummy"
             -  ``credentials_file`` doesn't overlap with other
                file names in ``mobile-dep`` - the convention is
                ``${root}/$product.p12``
             -  ``certificate_alias`` is ``$product``
             -  ``digest_algorithm`` matches your algorithm from step 1
             -  Checks that aren't relevant to your product are skipped
             -  Any other necessary properties are set (look at existing config for other
                products to see what the potential options are)

          3. In ``$pushapk_scriptworker_env`` for ``mobile-prod``, add a
             dictionary to ``$product_config`` such that:

             -  The ``product_names`` list includes ``$product``
             -  If you will have multiple apps on Google Play (e.g.:
                nightly app, beta app, production app), use the ``apps``
                block. Otherwise, set ``override_channel_model`` to
                ``single_google_app`` and use ``app`` (see Focus for an example)
             -  ``package_names`` includes your app's package name
             -  ``service_account`` set to
                ``$google_play_accounts['$product(-$channel)']['service_account']``
             -  ``credentials_file`` doesn't overlap with other
                file names in ``mobile-prod`` - the convention is
                ``${root}/$product(_$channel).p12``
             -  ``certificate_alias`` is ``$product``
             -  ``digest_algorithm`` matches your algorithm from step 1
             -  Checks that aren't relevant to your product are skipped
             -  Any other necessary properties are set (look at existing config for other
                products to see what the potential options are)

       3. In ``manifests/init.pp``

          1. For both ``mobile-dep`` and ``mobile-prod``, add an entry
             for each app on Google Play

       4. In ``manifests/jarsigner_init.pp``, for both ``mobile-dep``
          and ``mobile-prod``:

          1. Set a variable at the top of the section that points to the
             relevant certificate location
          2. Add an entry to the ``file`` block so that, at the
             certificate location, the source of the correct ``pem``
             file is copied in
          3. Add an entry to the ``java_ks`` block for your product,
             setting ``certificate`` to your certificate location

       5. In ``files/requirements.txt``

          1. From step 9, update the version of ``scriptworker``

8. Commit and push your ``build-puppet`` changes, make a PR

9. Once step 11's PR is approved, merge the ``build-puppet`` PR

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
    product, put the associated secrets in Hiera

    1. Connect to VPN and SSH into the puppet master
    2. Encrypt the ``service_account`` (you'll have been emailed or
       slacked a google service account: it looks like an email address
       that ends in ``gserviceaccount.com``)

       -  ``sudo eyaml encrypt --pkcs7-private-key /etc/hiera/keys/private_key.pem --pkcs7-public-key /etc/hiera/keys/public_key.pem --output examples -p -l 'service_account'``

    3. The google play p12 key is a binary file, so needs a couple more
       steps to be
       `encrypted <https://wiki.mozilla.org/ReleaseEngineering/PuppetAgain/Secrets#Using_EYAML>`__:

       1. In a new terminal, decrypt the p12 key (it should've been
          encrypted with your GPG key when sent to you via Slack or
          email)
       2. ``scp`` the file to the server:
          ``scp $p12file releng-puppet2.srv.releng.mdc1.mozilla.com:~``
       3. SSH into the puppet master
       4. ``sudo eyaml encrypt --pkcs7-private-key /etc/hiera/keys/private_key.pem --pkcs7-public-key /etc/hiera/keys/public_key.pem --output examples -f $p12file -l 'certificate'``

    4. ``sudo cp /etc/hiera/secrets.eyaml /etc/hiera/secrets.eyaml.$username``,
       substituting your username in to back up the hiera secrets file
    5. ``sudo vi /etc/hiera/secrets.eyaml``, replace the dummy
       ``service_account`` and ``certificate`` values

       -  Reminder to properly indent these values to match other Google
          Play credentials in the file

    6. ``shred -u $p12file`` to securely clean up the plaintext p12 key
       on the puppet master
    7. ``shred -u $p12file`` wherever you decrypted it on your machine
       (you may need to install ``shred``)

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

How to set up taskgraph for mobile
==================================

Setting up taskgraph for mobile is similar to setting up taskgraph for any
standalone project, especially github standalone projects: install
`taskgraph <https://hg.mozilla.org/ci/taskgraph>`__ in a virtualenv.

⚠️ You shouldn't install ``gradle`` globally on your system. The `./gradlew` scripts in each mobile repo define
specific gradle versions and are in charge of installing it locally.

On mac, using homebrew:

1. Install jdk8::

    brew tap homebrew/cask
    brew cask install homebrew/cask-versions/adoptopenjdk8

2. Install android-sdk::

    brew cask install android-sdk

3. Make sure you're pointing to the right java::

    # in your .zshrc or .bashrc
    export JAVA_HOME="$(/usr/libexec/java_home -v 1.8)"

    # After sourcing that file, you should get the following version:
    # > $JAVA_HOME/bin/java -version
    # openjdk version "1.8.0_265"
    # OpenJDK Runtime Environment (AdoptOpenJDK)(build 1.8.0_265-b01)
    # OpenJDK 64-Bit Server VM (AdoptOpenJDK)(build 25.265-b01, mixed mode)

4. test it::

    # In, say, an android-components clone, this should work:
    ./gradlew tasks --scan

    # And taskgraph optimized should return hundreds of tasks:
    # (You need https://hg.mozilla.org/build/braindump/ cloned)
    taskgraph optimized -p ../braindump/taskcluster/taskgraph-diff/params-android-components/main-repo-release.yml | wc -l

5. For ``taskgraph-gen.py`` to work, you'll also need to set ``ANDROID_SDK_ROOT``::

    # in your .zshrc or .bashrc
    export ANDROID_SDK_ROOT=/usr/local/Caskroom/android-sdk/4333796

6. You'll need a py2 virtualenv with taskgraph, glean-parser, and mozilla-version as well. To run ``taskgraph-gen.py``::

    # set $TGDIR to the braindump/taskcluster directory path
    TGDIR=..

    # Fenix
    $TGDIR/taskgraph-diff/taskgraph-gen.py --halt-on-failure --overwrite --params-dir $TGDIR/taskgraph-diff/params-fenix --full fenix-clean 2>&1 | tee out

    # Android-Components
    $TGDIR/taskgraph-diff/taskgraph-gen.py --halt-on-failure --overwrite --params-dir $TGDIR/taskgraph-diff/params-android-components --full ac-clean 2>&1 | tee out
