Releng 101
==========

What is this?
-------------

* a primer for understanding the Mozilla Release Engineering system. It strips down our infrastructure into bare essentials
* a series of 'walk-throughs' to help connect our concepts, technologies, environments, and src code
* provides stripped down snippets that represent real source from our repos.

What this is not
----------------

* documentation. We are moving with a strong emphasize to documenting our logic in the src itself. These are tutorials that can not be
  expressed in the code
* explanation of technologies we use. Each walk-through will explain how we use technologies but will point to :ref:`software` for overviews
* an in depth coverage of all our special edge cases, variants, conditions, and the like.

I hope this provides
--------------------

1. a life jacket for Mozilla Releng contributors and new-hires
2. a bridge between the abstract concepts and the physical code
3. confidence for exploring every dark corner of our releng universe

Releng in a Nutshell
--------------------

To get the ball rolling, below are a collection of materials that will help provide a Releng Overview

* `Release Engineering as a Force Multiplier`_ -- John O'Duinn's Keynote at ICSE 2013
* `Keep Calm and Ship It`_ -- Mozilla Releng through John Zeller's 2012 intern presentation
* `Mozilla's cloud and in-house continuous integration`_ -- Armen Zambrano's Releng Conf 2014 talk on recent cloud integration
* `Planet Releng`_ -- an aggregate of all Mozilla Releng's blog sites


The Walk-through series at a glance
-----------------------------------

1. :ref:`Checkin-To-Builds` - a tour through Buildbot (`latest update`__ if your not reading this online.)

__ https://github.com/mozilla/build-relengdocs/commits/master/releng101/checkin-to-builds.rst

2. *Building Firefox in automation* - harnessing Mozharness
3. *Setting up and configuring our machines* - becoming the master of Puppet
4. *Monitoring and nagging when things go wrong* - keeping an eye on our machines with BuildAPI, SlaveAPI, Slave Health, and Nagios
5. *Integrating the Cloud* - a look at our Cloud Tools
6. *Release Process* - explains why we hold the title of 'Release Engineers'
7. *Handling application updates* - Balrog to the rescue
8. *Serving your own machines* - loaning and allocating our machines through Selve-serve
9. *Syncing with HG and Git* - understanding vcs-sync
10. *Where to go from here* - tips on exploring our infrastructure: wikis, bugzilla, mxr, emails, irc, etc
11. *A look into the future* - what's up and coming: taskcluster, relengAPI, etc


    Template for new pages:

    * Software:
    * Repos:
    * Purpose of walk-through:

.. _Release Engineering as a Force Multiplier: https://www.youtube.com/watch?v=7j0NDGJVROI
.. _Keep Calm and Ship It: https://air.mozilla.org/intern-presentation-zeller/
.. _Mozilla's cloud and in-house continuous integration: https://air.mozilla.org/problems-and-cutting-costs-for-mozillas-hybrid-ec2-in-house-continuous-integration/
.. _Planet Releng: http://planet.mozilla.org/releng/
