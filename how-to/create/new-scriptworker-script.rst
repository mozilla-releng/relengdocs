New Scriptworker-Script
=======================

This procedure is based on the experience of `adding the pushmsixscript to scriptworker-scripts. <https://bugzilla.mozilla.org/show_bug.cgi?id=1745203>`__

* Write your new script and `add it to scriptworker-scripts <https://github.com/mozilla-releng/scriptworker-scripts/>`__.

 - You may want to clone-and-modify `an existing script <https://github.com/mozilla-releng/scriptworker-scripts/tree/master/pushmsixscript>`__.
 - Consult the :external+scriptworker-scripts:doc:`documentation <index>`.
 - Write unit tests for your script; you can run them locally with tox.

* Add clients to ci-configuration repo

 - `Example <https://hg.mozilla.org/ci/ci-configuration/rev/6870d0055a1d49e8d876010416b02e05b304b804>`__

* Add a new yaml file for your script's secrets to the `sops repo <https://source.developers.google.com/p/moz-fx-relengworker-prod-a67d/r/secrets-sops-relengworker>`__.

 - You may want to clone-and-modify an existing file.
 - ed25519PrivateKey is the same for all scripts.
 - Populate taskclusterAccessToken by resetting the access token for each client in the `taskcluster UI <https://firefox-ci-tc.services.mozilla.com/auth/clients>`__: open each of your clients, use the ... menu in lower right, select "reset access token", then scroll up to see the alert.

* Add your configuration parameters to cloudops-infra, like `this <https://github.com/mozilla-services/cloudops-infra/pull/3652>`__.

 - Reference those parameters in your script's `init_worker.sh <https://github.com/mozilla-releng/scriptworker-scripts/blob/master/pushmsixscript/docker.d/init_worker.sh>`__ and `worker.yml <https://github.com/mozilla-releng/scriptworker-scripts/blob/master/pushmsixscript/docker.d/worker.yml>`__. `Example <https://github.com/mozilla-releng/scriptworker-scripts/pull/451>`__.

* Ask SRE to `create a repo on hub.docker.com <https://bugzilla.mozilla.org/show_bug.cgi?id=1745203#c7>`__ for your new script.

* Try pushing to your script's dev branch:

 - git push origin master:dev-<your-script>

* Add entries to k8s-autoscale like `this <https://github.com/mozilla-releng/k8s-autoscale/pull/123>`__.

 - The :external:doc:`docs <scriptworkers-autoscaling>` may be helpful.
 - Merging will automatically trigger a dev deploy.
 - Be sure to deploy k8s-autoscale to production as well.

* When you are ready to start running tasks with your new script, add configuration to taskcluster, like `this <https://hg.mozilla.org/mozilla-central/rev/b236557131cd>`__.

