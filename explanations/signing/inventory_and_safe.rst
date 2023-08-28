Inventory and Archival
======================

It's best practice to inventory all of our signing materials at the `Signing Mana page <https://mana.mozilla.org/wiki/display/RelEng/Signing>`__, with instructions on how to generate new ones.

For expiry reminders, as of 2022.03.30 we file an issue against `RELENG-801 <https://mozilla-hub.atlassian.net/browse/RELENG-801>`__ and add a due date that matches the expiration date. We have automation to raise this issue a month before.

Archival in the Safe
--------------------

For private key material, we keep a backup for disaster recovery purposes. This is double-encrypted so no one team can access the secrets without the help of another team. Instructions are `here <https://mana.mozilla.org/wiki/display/SRE/Security+Operations+Secret+backup+service#SecurityOperationsSecretbackupservice-Safelocationsandcontent>`__. The line that says ``For an inventory of keys held in escrow`` contains a link to a GDrive that Releng has access to view.
