Firefox-CI ETL
==============

The :doc:`/explanations/fxci-etl` gathers data related to the Firefox-CI
Taskcluster instance and stores it in a series of BigQuery tables. When making
changes to the ETL, it's important to test them before pushing to production.

Most likely, changes will be in the `docker-etl`_ repository.

There are staging versions of all the components:

1. A GCS `bucket`_ in ``moz-fx-dev-releng``
2. A `BigQuery dataset`_ in ``moz-fx-dev-releng``
3. A `service account`_ with access to both, as well as read access to the L1
   and L3 workers projects (for obtaining metrics from Google Cloud Monitoring).
4. You must supply your own pulse account.

Setup
-----

Before you begin testing, you'll need to:

1. Create a new user via `Pulse Guardian`_ (if you don't already have one).
2. Clone https://github.com/mozilla/docker-etl
3. Then run:

   .. code-block:: bash
   
      cd jobs/fxci-taskcluster-export
      cat << EOF > config.dev.toml
      [pulse]
      user = "<pulse username>"
      password = "<pulse password>"
   
      [storage]
      project = "moz-fx-dev-releng"
      bucket = "fxci-etl-dev"
   
      [bigquery]
      project = "moz-fx-dev-releng"
      dataset = "fxci_etl_dev"
      EOF

4. Finally login to GCP with the `GCloud CLI`_:

   .. code-block:: bash
   
     gcloud auth login --update-adc
   
   The above requires that your personal credentials have access to all the
   necessary resources. There's also a `service account`_ you can use if
   needed.


Running the ETL
---------------

Setup the virtualenv:

.. code-block:: bash

   uv venv
   uv pip install -r requirements/test.txt
   uv pip install -e .

Run fxci-etl:

.. code-block:: bash

   uv run fxci-etl --help

Depending on what you're testing, there are currently two subcommands you'll
be interested in:

.. code-block:: bash

   # processes the pending messages in the pulse queues and inserts them into BQ
   fxci-etl pulse drain --config config.dev.toml

   # ingests data from Google Cloud Monitoring and exports it to BQ
   fxci-etl metric export --config config.dev.toml

.. important::

   The ETL does not currently clean up the pulse queues after itself (by design),
   and running ``fxci-etl pulse drain`` will automatically create all the necessary
   queues if they don't exist. So if you run this, you MUST manually delete them via
   PulseGuardian after you are done, otherwise they will grow indefinitely and cause
   issues for the pulse server.

After running, inspect the `moz-fx-dev-releng.fxci_etl_dev` dataset in the GCP
console and verify there is data. The tables under this dataset will
automatically be re-created by the ETL if they don't exist, so feel free to
delete them if you want a fresh start.

.. _docker-etl: https://github.com/mozilla/docker-etl/blob/main/jobs/fxci-taskcluster-export
.. _bucket: https://console.cloud.google.com/storage/browser/fxci-etl-dev;tab=objects?forceOnBucketsSortingFiltering=true&project=moz-fx-dev-releng&prefix=&forceOnObjectsSortingFiltering=false
.. _BigQuery dataset: https://console.cloud.google.com/bigquery?ws=!1m4!1m3!3m2!1smoz-fx-dev-releng!2sfxci_etl_dev
.. _service account: https://console.cloud.google.com/iam-admin/serviceaccounts/details/117200169815467733931/logs?project=moz-fx-dev-releng
.. _Pulse Guardian: https://pulseguardian.mozilla.org/
.. _GCloud CLI: https://cloud.google.com/sdk/docs/install
