==========================
Apple Store Administration
==========================

Changing the Account Holder
===========================

Context
-------

The Account Holder is a personal account that has unique access to the store. We cannot make it
a team/mailing account, Apple wants a physical person to own it. The account holder has
admin rights plus rights to accept terms of service and provide tax information, for
instance. Such rights are needed when you want to ship paid apps like the Firefox VPN.

Procedure
---------

1. As an admin, grant the future Account Holder admin rights.

2. As the future Account Holder, make sure you have Apple 2FA enabled. This is not the SMS-flavored 2FA, you need to own an Apple device that is tied to your work account. In order to be sure you enabled it, log back in to https://appstoreconnect.apple.com and see what 2FA method you are presented. If you don't get any SMS, then you're all set.

3. As the current Account Holder, go to https://developer.apple.com/account/#/membership/ and select "Transfer your Account Holder role" (see screenshot). This will trigger a procedure that involves humans and an identity check of the future Account Holder.

.. image:: /procedures/media/apple_account_holder.png

4. To be continued...


Responding to Employee Departures
=================================

Context
-------

When an employee leaves the company we must remove them from Mozilla's Apple Developer account. There is
a mailing list that is updated when this happens (ask someone for details), so we don't need to go
seek out this information ourselves.

Procedure
---------

1. Log in to the Apple Developer Account with the Apple Agent account.

2. Go to the ``People`` section of App Store Connect: https://appstoreconnect.apple.com/access/users

3. Search the user list for both the departing employees first name, last name, and e-mail address (they may have one or more accounts - so be careful).

4. Reply to the e-mail stating whether or not apple accounts were removed, eg: "2 apple developer accounts removed" or "no apple developer accounts found"
