win32-win64 migration
=====================

These steps are meant to be specifically for Firefox and Devedition
56.0b9.

High-level steps
~~~~~~~~~~~~~~~~

1. Create a new release in balrog for the migration
2. Create a new balrog rule on the cdntest channels to point to to the
   release blob

Detailed descriptions
~~~~~~~~~~~~~~~~~~~~~

After we have b9 release blobs available in balrog we need to create a
new release in balrog for win64 migration. We also need to create a new
watershed to map to this newly release in balrog so win32 users with
certain criteria will be updated to win64 firefox. See `bug
1393447 <https://bugzilla.mozilla.org/show_bug.cgi?id=1393447>`__ for
more details.

Download `the script
here <https://bug1393447.bmoattachments.org/attachment.cgi?id=8902074>`__
to munge the release blobs called munge.py

Login to `balrog admin <https://aus4-admin.mozilla.org>`__

Firefox beta
~~~~~~~~~~~~

Creating a new release in balrog
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Go to the `Firefox release for
   56.0b9 <https://aus4-admin.mozilla.org/releases#Firefox-56.0b9>`__
2. Select download to download the release blob
3. ``python munge.py /Users/kmoir/Downloads/Firefox-56.0b9-build1.json``
   which creates Firefox-56.0b9-build1-win64-migration.json
4. In balrog add a new release where name is
   Firefox-56.0b9-build1-win64-migration and product is firefox

Adding new rule
~~~~~~~~~~~~~~~

1. Add a rule to Firefox,beta-cdntest that points to that new rule. It
   should look like the top rule `in this
   screenshot <https://bug1393447.bmoattachments.org/attachment.cgi?id=8902907>`__
   except it should be on the beta-cdntest rule. The mapping should be
   to b9 win64 migration release you just added. The buildid should be
   updated to reflect the b9 buildid in the release blob. The comment
   should say b9 instead of b7. You don’t require signoff for rules in
   test channels so it will just be added.

Devedition beta
~~~~~~~~~~~~~~-

Modifying release blob
~~~~~~~~~~~~~~~~~~~~~~

1. Go to the `Devedition release for
   56.0b9 <https://aus4-admin.mozilla.org/releases#Devedition-56.0b9>`__
2. Select download to download the release blob
3. ``python munge.py /Users/kmoir/Downloads/Devedition-56.0b9-build1.json``
   which creates Devedition-56.0b9-build1-win64-migration.json
4. In balrog add a new release where name is
   Devedition-56.0b9-build1-win64-migration and Product is Firefox and
   upload your Devedition-56.0b9-build1-win64-migration.json file

.. _adding-new-rule-1:

Adding new rule
~~~~~~~~~~~~~~~

1. Add a rule to Firefox,aurora-cdntest that points to that new rule. It
   should look like the `second rule in this
   screenshot <https://bug1393447.bmoattachments.org/attachment.cgi?id=8902907>`__
   except it should be on the aurora-cdntest rule. The mapping should be
   to b9 win64 migration release you just added. The buildid should be
   updated to reflect the b9 buildid in the release blob. The comment
   should say b9 instead of b7. You don’t need signoff for rules on the
   test channel so it will just be added.

Softvision QE should now be able to test the 56.0b9 Firefox and
Devedition builds on the beta-cdntest and aurora-cdntest channels.

Before the builds are pushed to the beta and aurora channel in balrog,
new watersheds need to be added on the beta and aurora channels. In this
case, you can use the existing release blobs you created for testing on
the cdntest channel as the mapping in your rules. You need to create
rules on the beta and aurora test channels that look like this `in this
screenshot <https://bug1393447.bmoattachments.org/attachment.cgi?id=8902907>`__,
with the caveats that the buildid, mapping, and comment should be
updated to reflect the values for b9. Since these rules are on
production channels, you’ll need to add these rules as scheduled changes
and get signoff from QE, relman and releng.

Softvision QE should now be able to test the 56.0b9 Firefox and
Devedition builds on the beta aurora channels once they are enabled.
