How to automate nightly Google Play deployments
===============================================

These instructions define how to set up an Android product for nightly
deployment to the Google Play store. Additionally, to enable testing of
this automation before it's accepted, this documentation will guide how
to set up a staging pipeline.

Throughout this document, wherever the term ``$product`` is used,
substitute your product's name in (replacing spaces with hyphens), e.g.:
``reference-browser`` or ``fenix``.

Note: we don't need to explicitly "create" scopes in Taskcluster. We'll
simply tell Taskcluster that our hook *has* some scopes, then later
we'll tell it that we'll need those scopes to run our builds.
Taskcluster will just verify that the scopes we're using dynamically
match between the build and the hook that starts the build.

Note: we will soon move scope administration to
`ci-admin <https://hg.mozilla.org/build/ci-admin/>`__ rather than
administrating them in the live Taskcluster website.

1.  Request signing keys (example bug for
    ```reference-browser`` <https://bugzilla.mozilla.org/show_bug.cgi?id=1508761>`__).
    Confirm with the app's team what the "signature algorithm" and
    "digest algorithm" should be, and include that information in the
    ticket.

    -  You'll want at least one "dep" key for testing, as well as a
       separate "release" key for every separate app that will be
       created (e.g.: ``nightly``, ``beta`` and ``production``)

2.  Clone the product's repository

    -  While doing "staging" runs, it's easiest to use your ``master``
       branch so that checking it out for builds is straightforward.

3.  Add ``.taskcluster.yml`` in the root of the repository if it doesn't
    exist, and add a task for cron jobs. (```fenix``
    example\` <https://github.com/mozilla-mobile/fenix/blob/master/.taskcluster.yml>`__)

    1. Update the ``event.repository.html_url`` checks to use the
       correct repo URL
    2. Update scopes to be relevant for your product
    3. Update the apks in ``payload.command`` so that the paths match
       your product
    4. Update ``payload.image`` so that a compatible docker image is
       used
    5. Update ``metadata`` for your product

4.  In ``automation/taskcluster``, add ``decision_task_nightly.py``,
    ``schedule_nightly_graph.py`` and ``lib/tasks.py`` that will perform
    most of the automation wiring. (```fenix``
    examples <https://github.com/mozilla-mobile/fenix/blob/master/automation/taskcluster/>`__)

    1. ``schedule_nightly_graph.py`` is mostly good as-is, but I'd
       recommend a once-over to make sure there's nothing Fenix-specific
    2. Quite a few changes in the others: scopes, repositories, docker
       image
    3. There may be other useful tools in ``fenix``'s
       ``automation/taskcluster`` directory, such as ``gradle``
       functions or data structures to represent Android variants
    4. Once the rest of the infrastructure is set up, you can lean on
       "staging builds" to be confident that everything is configured
       correctly

5.  Create staging hook (e.g.:
    ```fenix-nightly-staging`` <https://taskcluster-web.netlify.com/hooks/project-mobile/fenix-nightly-staging>`__)

    1. Go to `Hooks <https://taskcluster-web.netlify.com/hooks>`__
    2. Click "Create Hook" at the bottom-right of the page
    3. ``HookGroupId`` is "project-mobile"
    4. ``HookId`` is ``$product-nightly-staging`` (e.g.:
       ``fenix-nightly-staging``)
    5. ``Name`` is "$product Nightly Builds (staging)"
    6. Add a ``Description`` if it can be more descriptive than the
       ``Name``
    7. ``Owner`` is different for each product, ask the product's team
       which email address they'd like to receive build failure
       notifications from
    8. Use the template from
       ```fenix-nightly`` <https://taskcluster-web.netlify.com/hooks/project-mobile/fenix-nightly>`__
       with some modifications:

       1. Use the correct ``payload.image``
       2. Update the ``payload.command`` to clone and run the correct
          repository
       3. Update the ``metadata``
       4. ``scopes`` should be ``assume:hook-id:project-mobile/$hookId``
          (using the ``HookId`` you defined above)

6.  Do the same thing, but for non-staging nightlies (e.g.:
    ```fenix-nightly`` <https://taskcluster-web.netlify.com/hooks/project-mobile/fenix-nightly>`__):

    1. ``HookId`` should be ``$product-nightly``
    2. ``Name`` should not end with "(staging)"
    3. Copy the task template from the staging hook, with some
       modifications

       1. Remove the ``--staging`` parameter from ``payload.command``
       2. Update ``metadata`` to remove anything mentioning "staging"
       3. Update the scope to assume from the non-staging hook's role

7.  Create the role for the staging hook (e.g.:
    ```fenix-nightly-staging`` <https://taskcluster-web.netlify.com/auth/roles/hook-id%3Aproject-mobile%2Ffenix-nightly-staging>`__)

    1. Go to `Roles <https://taskcluster-web.netlify.com/auth/roles>`__
    2. ``RoleId`` should be idential to your staging hook's ``HookId``,
       but prefixed with ``hook-id:`` (e.g.:
       ``hook-id:project-mobile/fenix-nightly-staging``)
    3. ``Description`` should be something like "Hook for building,
       signing and uploading (staging) Nightly versions of $product"
    4. Add all the scopes you'll need to fulfill the requirements in you
       ``.taskcluster.yml`` file (when ``is_mozilla_mobile_repo`` is
       ``false``)

8.  Do the same thing, but for non-staging nightlies (e.g.:
    ```fenix-nightly`` <https://taskcluster-web.netlify.com/auth/roles/hook-id%3Aproject-mobile%2Ffenix-nightly>`__)

    1. Remove mentions of "staging" from each field
    2. Make sure that all scopes are provided to fulfill requirements in
       ``.taskcluster.yml`` (when ``is_mozilla_mobile_repo`` is
       ``true``)

9.  Update ``scriptworker`` (`example for
    ``fenix`` <https://github.com/mozilla-releng/scriptworker/pull/298>`__)

    1. Add your product to ``_ALLOWED_MOBILE_GITHUB_OWNERS``
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
       7. Publish to ``Pypi``:

          1. ``gpg --list-secret-keys --keyid-format long`` to get your
             GPG identity (it's the bit after "sec rsaxxxx/"). An
             example GPG identity would be ``5F2B4756ED873D23``
          2. ``twine upload --sign --identity $identity dist/*`` to
             upload to Pypi (you may need to ``pip install twine``
             first)

10. Update configuration in
    ```build-puppet`` <https://github.com/mozilla-releng/build-puppet/>`__

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
       4. Later, in step 19, you'll have been emailed a Google Play
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
             -  ``google_credentials_file`` doesn't overlap with other
                file names in ``mobile-dep`` - the convention is
                ``${root}/$product.p12``
             -  ``certificate_alias`` is ``$product``
             -  ``digest_algorithm`` matches your algorithm from step 1
             -  Checks that aren't relevant to your product are skipped

          3. In ``$pushapk_scriptworker_env`` for ``mobile-dep``, add a
             dictionary to ``$product_config`` such that:

             -  The ``product_names`` list includes ``$product``
             -  If you will have multiple apps on Google Play (e.g.:
                nightly app, beta app, production app), use the ``apps``
                block. Otherwise, set ``map_channels_to_tracks`` to
                ``true`` and use ``single_app_config``
             -  ``package_names`` includes your app's package name
             -  ``service_account`` set to
                ``$google_play_accounts['$product(-$channel)']['service_account']``
             -  ``google_credentials_file`` doesn't overlap with other
                file names in ``mobile-prod`` - the convention is
                ``${root}/$product(_$channel).p12``
             -  ``certificate_alias`` is ``$product``
             -  ``digest_algorithm`` matches your algorithm from step 1
             -  Checks that aren't relevant to your product are skipped

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

11. Commit and push your ``build-puppet`` changes, make a PR

12. Test your automation with staging releases

    1. Synchronize your changes with the "dep" workers

       1. Confirm with the releng team that nobody is using the dep
          signing or pushapk workers
       2. SSH into the puppet master
       3. Follow the `instructions for setting up a puppet
          environment <https://wiki.mozilla.org/ReleaseEngineering/PuppetAgain/HowTo/Set_up_a_user_environment>`__

          1. Start with the `git
             section <https://wiki.mozilla.org/ReleaseEngineering/PuppetAgain/HowTo/Set_up_a_user_environment#Git>`__

             -  Don't forget to checkout the branch you just pushed in
                step 11

          2. Then `master machine
             setup <https://wiki.mozilla.org/ReleaseEngineering/PuppetAgain/HowTo/Set_up_a_user_environment#On_the_master_machine>`__
          3. Then
             `pin <https://wiki.mozilla.org/ReleaseEngineering/PuppetAgain/HowTo/Set_up_a_user_environment#Pinning>`__
             both the pushapk worker
             (``dep-m-pushapkworker-1.srv.releng.use1.mozilla.com``) and
             the signing worker
             (``dep-m-signing-linux-1.srv.releng.use1.mozilla.com``)
          4. For both the workers, SSH into them and `synchronize them
             with the environment you just
             created <https://wiki.mozilla.org/ReleaseEngineering/PuppetAgain/HowTo/Set_up_a_user_environment#On_the_worker_node.28s.29>`__

    2. In `Hooks <https://taskcluster-web.netlify.com/hooks>`__, go to
       the staging hook you created earlier
    3. Run a staging build

       1. Click "Trigger Hook" at the bottom of the page
       2. Under "Last Fired Result" (near the top), click the link
       3. Once the build is finished, go to the log, scroll to the
          bottom and copy the generated ID (to the right of the "RESULT"
          text)
       4. Go to `Task
          Groups <https://taskcluster-web.netlify.com/tasks/groups>`__
          and search with the value you copied

    4. Once all builds are passing, your automation is working!

13. Once step 11's PR is approved and the build is working in step 12,
    merge the ``build-puppet`` PR

14. Verify with app's team how ``versionCode`` should be set up. Perhaps
    by date like
    ```fenix`` <https://github.com/mozilla-mobile/fenix/blob/master/automation/gradle/versionCode.gradle>`__?

    -  Note that if there's multiple build types, they need different
       version codes. In the case of
       ```fenix`` <https://github.com/mozilla-mobile/fenix/blob/master/app/build.gradle#L50-L52>`__,
       ``x86`` builds have the version code incremented by 1.

15. When the Google Play product is being set up, an officially-signed
    build with a version code of 1 needs to be built. So, the main
    automation PR for the product will need to be stunted: it needs to
    produce APKs with a version code of 1, and it should have pushing to
    Google Play disabled (so we don't accidentally push a build before
    our official version-code-1 build is set up).

    1. Change the version code to be set to 1. If the product uses the
       same version-code-by-date schema as ``fenix``, then edit
       ```versionCode.gradle`` <https://github.com/mozilla-mobile/fenix/pull/156/files#diff-63606bb315fadc051f73a54767849985R41>`__
    2. `Disable the creation of the task that pushes to Google
       Play <https://github.com/mozilla-mobile/fenix/pull/156/files#diff-73e51d972c105de5122ec559909980daR123>`__
    3. Create the PR
    4. Once approved, merge the PR

16. Verify the apk artifact(s) of the signing task

    1. Trigger the non-staging hook
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

17. Request both the creation of a Google Play product and for the
    credentials to publish to it. Consult with the product team to `fill
    out the requirements for adding an app to Google
    Play <https://wiki.mozilla.org/Release_Management/Adding_a_new_app_on_Google_play>`__.
    This request should be a bug for "Release Engineering > Release
    Automation: Pushapk", and should be a combination of
    `this <https://bugzilla.mozilla.org/show_bug.cgi?id=1508294>`__ and
    `this <https://bugzilla.mozilla.org/show_bug.cgi?id=1512173>`__

    -  As part of the bug, note that you'll directly send an APK to the
       release management point of contact via Slack

18. Give the first signed APK to the Google Play admins

    1. Perform a non-staging build
    2. Once the signing task is done, grab the APK with the version code
       of 1 (if there's multiple APKs, you probably want the arm one)

       -  You can verify the version code of the apk with
          `apktool <https://ibotpeaches.github.io/Apktool/>`__, then
          viewing the extracted ``AndroidManifest.xml`` and looking at
          the ``platformBuildVersionCode``

    3. Send the APK to release management

19. Once the previous step is done and they've set up a Google Play
    product, put the associated secrets in Hiera

    1. Connect to VPN and SSH into the puppet master
    2. Encrypt the ``service_account`` (you'll have been emailed or
       slack'd a google service account: it looks like an email address
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

20. Perform a new PR that un-stunts the changes from step 15 `Fenix
    example <https://github.com/mozilla-mobile/fenix/pull/161>`__

    -  Version code should be generated according to how the team
       requested in step 14
    -  The task that pushes to Google Play should no longer be disabled

21. Once the PR from the last step is merged, trigger the non-staging
    nightly task, verify that it uploads to Google Play

22. Update the ``$product-nightly`` hook, adding a schedule of
    ``0 12 * * *`` (make it fire daily)

    -  Ensure that the hook is triggered automatically by waiting a day,
       then checking the hook or indexes
