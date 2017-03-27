Releng Future Projects
======================

Similar to Taskcluster's `Round Tuit
Box <https://wiki.mozilla.org/TaskCluster/Round_Tuit_Box>`__, this is a
set of projects we'd love to tackle when we have time.

Ideas
~~~~~

Mac Signing on Linux
--------------------

Currently, we need to sign mac binaries on mac hardware, forcing us to
maintain a separate set of mac signing servers. Instead, if we're able
to sign mac binaries on linux, that allows us to use the same linux
signing servers. This may require porting some mac tools to linux; we're
leaning towards rust.

"Shippable" builds
------------------

Currently, we have depend builds which prioritize speed, and nightly/release builds which prioritize correctness.

We can combine nightly, release, and PGO builds into a single type, "shippable" builds.  These can run on any branch at the schedule of our choosing.  They're only shipped when we choose to promote these to the appropriate channel.  These will be clobber, PGO, multilocale, branded, etc.

Let's run depend builds on push and shippable builds periodically on integration branches.  On Try, either should be choosable using try syntax.  On release branches, let's build shippable builds on push and ignore depend opt builds.

Local depend signing
--------------------

Currently, we use the signing servers for depend signing, except on Android, where the Android tools create throwaway dev keys and sign any otherwise unsigned apk during packaging.

We're theorizing we might be able to do the same with other signing types, though key generation may be too time- and resource- costly.  Sharing of untrusted depend keys may be a way to solve this.

We could potentially use `docker-signing-server <https://github.com/escapewindow/docker-signing-server>`__ as a way to achieve this for everything but dmg signing.  This would allow the workflow to be closer to the nightly/release workflow.

Guidelines
~~~~~~~~~~

The ideas listed here should be multi-month projects, but should not
last forever (so, "build XYZ", but not "maintain ABC indefinitely").

They should be reasonably well-defined, and not require blue-sky design
or unproven technologies (so, no quantum computing, sorry).

Avoid linking to discussions. Link to (or just include here) succinct
descriptions of the current thinking about the idea.
