Profile Python Code
===================

Profiling is a handy way to find hot spots and other areas of your code to optimize. There are many tools available to profile python code. There are a few that we commonly use and recommend in RelEng. Each is described in further detail below, with pros and cons.

samply
------

`Samply <https://github.com/mstange/samply>`__ is a low overhead profiling tool that uses the Firefox Profiler to display traces. It tracks multiple processes and threads, and allows you to look at each individually over time. Because it is fairly comprehensive and quick to use, it is a good "go to" profiling tool if you're not sure what you need.

Once installed, you can run it by prefixing any regular python invocation with ``samply record -- PYTHONPERFSUPPORT=1``. For example:

::

   samply record -- PYTHONPERFSUPPORT=1 ./mach taskgraph tasks

Once the command is completed, samply will open the profile in your default browser. For help interpreting the data, refer to the `Firefox Profiler documentation <https://profiler.firefox.com/docs/#/>`__.

yapii
-----

TODO

./mach --profile-command
------------------------

Mach has its own handy profiling built-in. Under the hood, this uses `cProfile <https://docs.python.org/3/library/profile.html>`__, which means it will only follow the main python process, making it less useful for things like ``taskgraph`` that spawn multiple processes. Nevertheless, it can still be useful when profiling some ``mach`` commands to get a basic idea of where the hottest code is.

An example invocation is as follows:
::

   ./mach --profile-command try fuzzy

Once the command completes it will suggest you run the following to visualize the profile:
::

   python3 -m pip install snakeviz
   python3 -m snakeviz mach_profile_taskgraph.cProfile

Running that will open the profile in your default browser. Typically, sorting on ``cumtime`` will be a good first indication of which functions most of the time is being spent in. Refer to the `Snakeviz documentation <https://jiffyclub.github.io/snakeviz/#interpreting-results>`__ for additional details on interpretation.
