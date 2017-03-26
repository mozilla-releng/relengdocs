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

Guidelines
~~~~~~~~~~

The ideas listed here should be multi-month projects, but should not
last forever (so, "build XYZ", but not "maintain ABC indefinitely").

They should be reasonably well-defined, and not require blue-sky design
or unproven technologies (so, no quantum computing, sorry).

Avoid linking to discussions. Link to (or just include here) succinct
descriptions of the current thinking about the idea.
