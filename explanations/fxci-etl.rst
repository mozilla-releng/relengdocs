Firefox-CI ETL
==============

The Firefox-CI ETL is a data pipeline designed to expose data such as cost and
worker metrics to Firefox-CI stakeholders, to help them make informed decisions
about the operation and configuration of the Taskcluster instance.

Data
----

This ETL stores data into a number of tables in the ``moz-fx-data-shared-prod``
project. They are:

* `moz-fx-data-shared-prod.fxci_derived.tasks_v2`_
   * Primary key: ``task_id``
* `moz-fx-data-shared-prod.fxci_derived.task_runs_v1`_
   * Primary key: ``task_id``, ``run_id``
* `moz-fx-data-shared-prod.fxci_derived.worker_metrics_v1`_
   * Primary key: ``project``, ``zone``, ``instance_id``
* `moz-fx-data-shared-prod.fxci_derived.worker_costs_v1`_
   * Primary key: ``project``, ``zone``, ``instance_id``

.. _moz-fx-data-shared-prod.fxci_derived.tasks_v2: https://console.cloud.google.com/bigquery?project=moz-fx-data-shared-prod&ws=!1m5!1m4!4m3!1smoz-fx-data-shared-prod!2sfxci_derived!3stasks_v2
.. _moz-fx-data-shared-prod.fxci_derived.task_runs_v1: https://console.cloud.google.com/bigquery?project=moz-fx-data-shared-prod&ws=!1m5!1m4!4m3!1smoz-fx-data-shared-prod!2sfxci_derived!3stask_runs_v1
.. _moz-fx-data-shared-prod.fxci_derived.worker_costs_v1: https://console.cloud.google.com/bigquery?project=moz-fx-data-shared-prod&ws=!1m5!1m4!4m3!1smoz-fx-data-shared-prod!2sfxci_derived!3sworker_costs_v1
.. _moz-fx-data-shared-prod.fxci_derived.worker_metrics_v1: https://console.cloud.google.com/bigquery?project=moz-fx-data-shared-prod&ws=!1m5!1m4!4m3!1smoz-fx-data-shared-prod!2sfxci_derived!3sworker_metrics_v1

Components
----------

The ETL consists of several components spread across various repositories.

Docker Image and Python Module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A `taskcluster-fxci-export docker image`_ is defined in the
`mozilla/docker-etl`_ repository. Changes to this directory cause
the image to be re-built and pushed to Google Artifact Registry via CircleCI.

.. warning::
   As of this writing, a member of the data engineering team must merge the PR.
   Otherwise the image will be built by CI, but not pushed to Google Artifact
   Registry.

The image contains the `fxci-etl Python module`_, which
provides the ``fxci-etl`` binary containing subcommands to run any necessary
business logic pertaining to the Firefox-CI ETL. It is designed to be
extensible, so can be re-used for future needs.

See the `README`_ for information on supported configuration
and commands.

Telemetry Airflow DAGs
~~~~~~~~~~~~~~~~~~~~~~

Telemetry Airflow is the name of the `Apache Airflow`_ instance run by
Mozilla's data infrastructure team.

There are two Firefox-CI ETL related `DAGs`_ defined in
the `telemetry-airflow`_ repo. These DAGs use the aforementioned docker image
to run an `fxci-etl`_ command on a cron schedule. The DAGs are:

1. `fxci_pulse_export`_ - This DAG is
responsible for draining some Taskcluster pulse queues and inserting records
into the ``tasks_v2`` and ``task_runs_v1`` BigQuery tables.

2. `fxci_metric_export`_ - This DAG is
responsible for querying metrics from Google Cloud Monitoring (namely worker
uptime for now), and inserting records into the ``worker_metrics_v1``
BigQuery table.

The DAGs use the latest version of the image, so no changes are required

Derived Tables
~~~~~~~~~~~~~~

Finally, there is a derived table that uses infrastructure in the
`bigquery-etl`_ repository.

This is simply defined in a `.sql file`_ and is used to extract
worker cost data from the GCP billing table and insert the result into the
``worker_costs_v1`` BigQuery table.

See this `bigquery-etl tutorial`_ for more information on
how the process works.

.. _Apache Airflow: https://airflow.apache.org/
.. _DAGs: https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html
.. _bigquery-etl: https://github.com/mozilla/bigquery-etl
.. _bigquery-etl tutorial: https://mozilla.github.io/bigquery-etl/cookbooks/creating_a_derived_dataset/
.. _mozilla/docker-etl: https://github.com/mozilla/docker-etl
.. _fxci-etl: https://github.com/mozilla/docker-etl/blob/main/jobs/fxci-taskcluster-export
.. _taskcluster-fxci-export docker image: https://github.com/mozilla/docker-etl/blob/main/jobs/fxci-taskcluster-export
.. _fxci-etl Python module: https://github.com/mozilla/docker-etl/blob/main/jobs/fxci-taskcluster-export/fxci_etl
.. _README: https://github.com/mozilla/docker-etl/blob/main/jobs/fxci-taskcluster-export/README.md
.. _telemetry-airflow: https://github.com/mozilla/telemetry-airflow
.. _fxci_metric_export: https://github.com/mozilla/telemetry-airflow/blob/main/dags/fxci_metric_export.py
.. _fxci_pulse_export: https://github.com/mozilla/telemetry-airflow/blob/main/dags/fxci_pulse_export.py
.. _.sql file: https://github.com/mozilla/bigquery-etl/blob/main/sql/moz-fx-data-shared-prod/fxci_derived/worker_costs_v1/query.sql
