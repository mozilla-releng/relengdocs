# Apple Certificates

Apple docs: https://developer.apple.com/support/certificates/

The process to create a new certificate signing request can be found here:
https://help.apple.com/developer-account/#/devbfa00fef7

Instructions on how to issue new certs:
https://mana.mozilla.org/wiki/pages/viewpage.action?spaceKey=RelEng&title=Signing#Signing-OSX&iOSSigning

### Notes
1. There's a limited amount of `Apple Distribution`, `Developer ID Installer`, 
`Developer ID Application`, `iOS App Development` (and possibly others) that can
be issued and valid at the same time.
**BE EXTREMELY CAREFUL WITH ISSUED CERTIFICATES.**

1. `App Managers` with `Access to Certificates, Identifiers & Profiles` are able
to issue production level certificates. We should avoid giving out this type of
access.

1. If we migrate to autograph/rcodesign, we won't need to hold the certificate in a keychain
