# Signing Cert Levels and Best Practices

## Levels / cert types

### Dep

The `dep`, aka `depend` certs, tend to be self-signed or otherwise non-shipping certs. (The name comes from the Netscape days, when `depend` builds were builds that pulled the latest CVS changes on top of the previous build's source without clobbering the objdir; `clobber` builds, which nuked and recloned the tree, were significantly slower but more likely to produce a shippable candidate build.)

We do bake in some of these keys into, say Firefox Nightly to allow for installing addons signed with the dep addon-signing keys, or for installing updates signed with the dep mar-signing key, so these keys aren't fully throwaway, but we tend to not be as concerned about the security of these keys.

Dep key generation varies by key format; we've documented it on the [mana page](https://mana.mozilla.org/wiki/pages/viewpage.action?spaceKey=RelEng&title=Signing#Signing-Acquiringkeys).

In general, any testing releng does should involve the dep certs, unless we're specifically testing something that requires a nightly or release cert.

### Shipping certs

In general, best practice would be to avoid using shipping certs for any testing if we can.

#### Nightly

In various products and signing types we differentiate Nightly versus Release signing.

In some cases, this is a hard split. For instance, MAR signing for Firefox desktop updates, uses separate keys for nightly vs release signing, and we verify which key signed an update before applying. This provides some security and some sanity checking to prevent shipping release updates off of nightly branches, at the cost of maintenance overhead. It may be worth revisiting whether the benefits outweigh the costs.

In other cases, we don't verify the signature; the OS verifies the signature. For instance, Windows or Mac signing. So we have a Nightly Mac cert and a Release Mac cert, but either would be valid for signing Nightly or Release Firefox for Mac, so this split may cause more maintenance work than it's worth.

#### Release

Release signing is generally our set of certs for our production release builds across products. (We may also need to add nightly certs and `production` certs for a full set of shipping certs.)

#### Production

In some mobile products, we use the `production-signing`, most likely as a mix of `release-` and `nightly-` signing. It may be worth renaming that to `release` if it's confusing.

## Caveats

### Android signatures

Historically, Google required that signing certs for Android applications be long-lived (15+ years IIRC), and did not allow for cert rotation. Essentially, if you have an APK signed with cert X, and you get an update that's signed with cert Y, it's treated as a completely different application. You can't update to the second APK; you need to uninstall and reinstall, and may lose your prefs or profile or associated downloads in doing so.

This changed with the [Android v3 signature scheme](https://www.xda-developers.com/apk-signature-scheme-v3-key-rotation/), which finally allows for cert rotation. However, older devices don't support v3 signatures, so as long as we want to support these older devices, we still cannot rotate our shipping Android certs.

Caveat: let's get the "which cert should we use" decision right *before* we ship an Android product for the first time, and let's not leak the key or anything that would mandate a key rotation.
