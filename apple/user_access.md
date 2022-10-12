# Apple Account User Access

All mozilla apple (mac/iOS) developers will need an apple account. We should try
as much as possible only give out permissions to their @m.c accounts. Personal
accounts should be avoided in case the developer leaves the company and we don't
delete the apple account.

## Permissions
Roles are confusing!

An user with `Developer` Role, and 
`Access to Certificates, Identifiers & Profiles` will only be able to access 
development-level items. **The majority of developers will want this combination.**

`App Managers` with `Access to Certificates, Identifiers & Profiles` will be able
to issue production-level certificates. **It is very unlikely that we should 
allow this type of access. Make sure the user understands this risk.**

Sales, Marketing and Finance users will likely want `Access to Reports`.
