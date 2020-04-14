Historic Release Promotion
==========================

This document describes automation for ESR52 and older branches.

Understanding release promotion
-------------------------------

-  this task is optional and refers to understanding how release
   promotion works
-  the original release workflow diagram before Buildbot -> Taskcluster
   migration, as to November 2015, can be found
   `here <https://www.lucidchart.com/documents/view/b733c8be-e607-445f-824a-f3353c287294>`__
-  the up-to-date version of it, as to September 2016, is itteratively
   divided in two. First graph depicts the logic pieces and all tasks in
   Taskcluster, but lacks the dependencies between the tasks within the
   graph, and can be found
   `here <https://www.lucidchart.com/documents/view/1b59f91d-1dfa-4d1e-8a50-d2d2759a3fff>`__
-  the follow-up version of it, with all the tasks and graph
   dependencies can be found
   `here <https://www.lucidchart.com/documents/view/29588c49-c18c-4800-be84-cca359d89ffc>`__

   -  A “higher level” diagram of the release process is also available
      in the `Releng
      docs <http://moz-releng-docs.readthedocs.io/en/latest/release_workflows/index.html>`__.

Requirements
------------

-  taskcluster-cli installed
-  releasewarrior-2.0 installed
-  ssh access to ``buildbot-master85.bb.releng.scl3.mozilla.com``

taskcluster setup
-----------------

To get credentials with 24h lifetime:
``$ eval $(taskcluster signin --scope 'queue:*')``

This sets environment variables so run taskcluster in the same terminal.

Actions for Desktop related releases
------------------------------------

1. push to releases dir (mirrors)
---------------------------------

why
~~~

-  some releases don’t automatically push releases to the releases dir
   automatically. They instead wait on a human decision (sign off) to
   dictate when candidates dir looks good and we are ready to copy/push
   to releases dir

when
~~~~

-  Desktop Firefox ESRs

   -  wait for sign off from release-signoff with email like:
      ``[desktop] Please push ${version} to {cdntest,releases,mirrors}``
      where version is like: ``52.0esr`` or ``52.2.0esr``, and channel
      is like: ``esr-cdntest`` or ``cdntest`` or ``mirrors`` or
      ``releases``

      -  note: if they do not explicitly ask for ``release-cdntest`` it
         is okay to assume if you are confident but please reply with
         something like
         ``pushed and please use explicit name when requesting next time: esr-cdntest channel :)``

how
~~~

-  Desktop Firefox ESRs

   -  ESR x.y.Z (ie chemspills/regression fixes) releases can use the
      jobs in the existing graph.

      -  get the taskid for the task named
         ``firefox mozilla-esr52 push to releases human decision task``
      -  This task is blocking
         ``[beetmover] firefox mozilla-esr52 push to releases``
      -  To resolve the human decision task run the following:
         ``taskcluster task complete $TASK_ID``

   -  ESR x.y.0 releases (ie scheduled) use two taskcluster graphs,
      because the push+shipping tasks will usually timeout in the
      original graph between building and release day. Pushing to
      releases happens in a graph 2 and will start once graph 2 is
      submitted.

      -  to generate and submit graph 2 of the release:

         -  step 1) get a taskid from a any task in graph 1. this is
            used by graph 2 for obtaining release version, branch, etc.
         -  step 2) call releasetasks_graph_gen.py and pass, among other
            things, the taskid obtained in step 1:

         .. code:: bash

            $ ssh `whoami`@buildbot-master85.bb.releng.scl3.mozilla.com  # host we release-runner and you generate/submit new release promotion graphs
            $ sudo su - cltbld
            $ TASK_TASKID_FROM_GRAPH1={insert a taskid from any task in graph 1}
            $ cd /home/cltbld/releasetasks/
            $ git pull origin master  # make sure we are up to date. note: make sure this is on master and clean first
            $ cd /builds/releaserunner/tools/buildfarm/release/
            $ hg pull -u # make sure we are up to date. note: make sure this is on default and clean first
            $ source /builds/releaserunner/bin/activate
            # call releasetasks_graph_gen.py with --dry-run and sanity check the graph output that would be submitted
            $ python releasetasks_graph_gen.py --release-runner-config=../../../release-runner.yml --branch-and-product-config=/home/cltbld/releasetasks/releasetasks/release_configs/prod_mozilla-esr52_firefox_rc_graph_2.yml --common-task-id=$TASK_TASKID_FROM_GRAPH1 --dry-run
            # call releasetasks_graph_gen.py for reals which will submit the graph to Taskcluster
            $ python releasetasks_graph_gen.py --release-runner-config=../../../release-runner.yml --branch-and-product-config=/home/cltbld/releasetasks/releasetasks/release_configs/prod_mozilla-esr52_firefox_rc_graph_2.yml --common-task-id=$TASK_TASKID_FROM_GRAPH1

2. signoffs
-----------



why
~~~

-  to guard against bad actors and compromised credentials we require
   that any changes to primary release channels (esr) in balrog are
   signed off on by at least two people.



when
~~~~

-  after the scheduled change has been created by the “updates” task,
   and prior to the desired publish time



how
~~~

-  through the Balrog Scheduled Changes UI
   (https://aus4-admin.mozilla.org/rules/scheduled_changes)

-  RelEng

   -  RelEng is responsible for reviewing the scheduled change to ensure
      that the mechanics are correct. Most notably, the mapping,
      fallbackMapping, and backgroundRate need to be verified.

-  RelMan

   -  RelMan is responsible for reviewing the scheduled change to ensure
      that the shipping time is correct and to authorize that the
      release may be shipped. If circumstances change (eg, we discover a
      bug we’re not willing to ship) after they sign off, they must
      revoke their signoff in Balrog.

example
~~~~~~~

After the Scheduled Change has been created, the Balrog UI will look
something like: |scheduled change without signoffs|

When RelEng reviews it they will look at the Mapping, Fallback Mapping,
and Backgound Rate (circled above). If everything looks good to them,
they will click on the “Signoff as…” button and be presented with a
dialog like: |signoff modal dialog|

After they make their Signoff, the primary UI will reflect that:
|scheduled change with one signoff|

RelMan and QE will go through a similar process. Once they make their
Signoffs the primary UI will reflect that as well: |scheduled change
with two signoffs|

Now that the Signoff requirements have been met, the Scheduled Change
will be enacted at the prescribed time.

3. publish release
------------------



why
~~~

-  the publish release human decision task triggers the balrog change
   submission, update bouncer aliases, mark as shipped, and bump version
   tasks
-  updates are published by Balrog when the scheduled change hits its
   scheduled time and all required signoffs have been completed.

   -  It is expected that RelEng and RelMan will sign off on the
      scheduled changes ahead of the ship date for .0 releases,
      otherwise ASAP after the change is submitted
   -  If the ship time, throttle rate, or anything else about the
      release changes between the change being scheduled and the
      expected ship time, the scheduled change should be updated (or
      deleted) to reflect the change. After doing so, Signoff will be
      required again.



when
~~~~

-  All Desktop Firefox releases

   -  Wait for email on the balrog-db-changes list that shows the
      mapping on the live channel being changed to the Release being
      shipped.



how
~~~

-  Desktop Firefox ESRs

   -  depending on timing you may have 1 or 2 graphs. Go to the latest
      one and find taskId of ``publish release human decision task``
   -  Resolve the “publish release human decision” task using the
      command below

   .. code:: bash

       taskcluster task complete $TASK_ID

4. post release step
--------------------



why
~~~

-  releases are needed to be marked as “shipped” in Ship-it to make the
   partial guessing algorithm work and make sure the product-details
   site has correct information about releases.



when
~~~~

-  immediately after running ``publish release`` human decision step



how
~~~

-  Desktop Firefox Betas, Desktop Firefox Release, Desktop Firefox dot
   Releases, Desktop Firefox ESRs and Fennec Beta/Releases

   -  it is done automatically so just sanity check that the
      ``<product> <channel> mark release as shipped`` has completed
      successfully in the graph

-  Other *not* release-promotion based releases (Thunderbird) are needed
   to be marked as shipped on Ship It. To do so, visit
   https://ship-it.mozilla.org/releases.html, find the release in
   question, and click the “Shipped!” button.

Troubleshooting
--------------=

Intermittent failures
---------------------

If a task failed because of an intermittent failure (e.g.: network
error, timeout), ``rerun`` it manually via `taskcluster
cli <https://github.com/taskcluster/taskcluster-cli/>`__. Some tasks
don’t have automatic reruns set, but they do have 5 retries left. Thanks
to reruns, you don’t need to retrigger a task (which would have meant to
reschedule the remaining subgraph).

Flushing caches
---------------

If more than one build ran on a beta we need to flush the caches to
remove the older builds from the CDN caches. For instance in Firefox
beta 46.0b5 we built builds 1 through 5 but we only ship build5. See
`Bug 1391843 <https://bugzil.la/1391843>`__ - Please purge CDN caches
for firefox and devedition 56.0b4 as an example. After filing the bug as
P1, it’s highly recommended you follow up with the `mana
docs <https://mana.mozilla.org/wiki/display/SVCOPS/Contacting+Cloud+Operations>`__
to contact CloudOps by email as well as they don’t always pay attention
to P1 bugs.

Working around Signoffs in Balrog
---------------------------------

The Required Signoffs we have implemented in Balrog are there for a
reason. In general, you should not try to workaround them. On occasion,
extreme circumstances may warrant doing so, however. The most likely
reason for this would be no members of a particular group being around,
and needing to make an urgent change (eg: shutting off updates).

Note that even if you are a full fledged administrator, you yourself
cannot make more than one Signoff on any given Scheduled Change. This is
by design - we do not want a single account to be able make changes to
protected Products or Channels. If you are certain you need to
workaround the Signoffs, here’s how: \* Find another person with some
permissions in Balrog, and who is up to speed on the change you intend
to make. \* Grant them the Role that you need to complete the Required
Signoffs (through https://aus4-admin.mozilla.org/permissions). \* Have
them make a Signoff with that Role.

As a concrete example, let’s say we required 1 relman, 1 releng, and 1
qe signoff for Firefox release channel changes. Late on a Saturday night
we discover a massive crash that requires us to shut off updates. Liz
gets in contact with Kim to ask that this happen. Kim Schedules the
necessary change in Balrog (which implicitly satisfies the releng
signoff), and Liz signs off for relman. Because it is the weekend, and
there was no planned work, QE is unavailable. Kim gets in contact with
Aki, grants him the “qe” role, and Aki makes a Signoff under the “qe”
Role, which fulfills the Signoff requirements. Kim then removes Aki’s
“qe” Role.

Creating a clone of a task using a different revision
-----------------------------------------------------

This works with tasks where the task is on the edge of the graph, and
has no dependencies. Example: create
https://tools.taskcluster.net/groups/Co8iBgS1RnKVNOWMZm0TUg/tasks/Co8iBgS1RnKVNOWMZm0TUg/details
by cloning the failed task (Actions -> Edit Task) and replaced all
revision entries with the new one

.. |scheduled change without signoffs| image:: /balrog/media/only_scheduled.png
.. |signoff modal dialog| image:: /balrog/media/signoff_dialog.png
.. |scheduled change with one signoff| image:: /balrog/media/one_signoff.png
.. |scheduled change with two signoffs| image:: /balrog/media/all_signoffs.png
