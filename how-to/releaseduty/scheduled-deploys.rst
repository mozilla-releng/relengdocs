Regularly Scheduled Deploys
===========================

We aim to deploy our most important systems every week. This includes `Balrog <https://github.com/mozilla/balrog>`__, `Ship It <https://github.com/mozilla-releng/shipit>`__, `scriptworkers <https://github.com/mozilla-releng/scriptworker-scripts>`__, `tooltool <https://github.com/mozilla-releng/tooltool>`__ and `k8s-autoscale <https://github.com/mozilla-releng/k8s-autoscale>`__.

The ``#releng-notifications`` channel in Slack is set-up with reminders to stage these deployments every Tuesday and push them to production every Thursday. You should check in with Release Management prior to performing production pushes to ensure that there are no ongoing critical releases. (We generally proceed with deployments regardless of regularly scheduled release activity, but chemspills will typically cause us to skip a week.)

Note: we skip the ``scriptworker`` staging deployments because nothing runs against those regularly, and pushing changes may interfere with people testing their own changes to scriptworkers.

Instructions for staging and deploying changes to production can be found with the documentation for each project. (`Balrog deployments <https://mozilla-balrog.readthedocs.io/en/latest/infrastructure.html#deploying-changes>`__, `Ship It deployments <https://github.com/mozilla-releng/shipit#deployed-environments>`__, `scriptworker dev <https://scriptworker-scripts.readthedocs.io/en/latest/scriptworkers-dev.html>`__ and `production <https://scriptworker-scripts.readthedocs.io/en/latest/scriptworkers-production.html>`__ deployments, `tooltool deployments <https://github.com/mozilla-releng/k8s-autoscale>`__, `k8s-autoscale deployments <https://github.com/mozilla-releng/k8s-autoscale#deployment>`__)
