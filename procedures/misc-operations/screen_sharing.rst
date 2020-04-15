Sharing your terminal
=====================

Introduction
------------

During some tasks it's useful to have more than one person present to
check commands before they are entered. This may be due to the severity
of an event and the risk if the commands are incorrect, or may be as
straightforward as running a tutorial.

While Vidyo can share screens (in the display sense), it's often not the
clearest for sharing a terminal window.

Screen
------

Setup
~~~~~

To enable multi-user screen sessions, the screen binary must be setuid

::

   chmod u+x /usr/bin/screen

To save time during the screen session, we can add the necessary options
to ``~/.screenrc`` of the user who will be setting up the session.

::

   multiuser on
   acladd user1,user2,user3
   screen -L

``multiuser`` allows a screen session to be connected to from several
places at once. ``acladd`` adds specific usernames to the list of
accounts allowed to connect to a screen session ``screen -L`` starts a
screen window with logging enabled.

If you don't want this configuration for every screen session, this can
also be saved as a separate configuration file, and screen run with
``screen -c configfile``

Usage
~~~~~

In this example, the ``cltbld`` user will be running a screen session,
and has ``~/.screenrc`` set up as above.

Use the ``-S`` option to give the shared screen a more useful name

::

   cltbld@host1:~> screen -S shared

As the other user:

::

   user1@host1:~> screen -x cltbld/shared

With ``-L`` the output logs of the screen shell will be saved in the
current working directory as ``screenlog.0`` with incrementing integers
if the file already exists. If you have colors turned on in your shell,
remember that you can use ``less -R`` to view this log file and render
the colors, instead of wading through pages of terminal coding.

Tmux
----

Single user, multiple connections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If two people are using a shared account, such as ``cltbld``, then tmux
doesn't require any setup.

To create a session:

::

   tmux new -s shared

To join an existing session:

::

   tmux attach -t shared

Multiple users
~~~~~~~~~~~~~~

For multiple users, tmux requires a socket directory that both users can
access, by being members of the same unix group.

::

   mkdir /tmp/tmux-share
   chgrp <shared-group> /tmp/tmux-share

To create a session:

::

   tmux -S /tmp/tmux-share new -s shared

To join an existing session

::

   tmux -S /tmp/tmux-share attach -t shared
