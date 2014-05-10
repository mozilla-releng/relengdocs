.. _Checkin-To-Builds:

From a change on a repo to builds being triggered
=================================================

* Software:

  + Buildbot - If you are new to Buildbot, please see :ref:`Buildbot`
* Repos:

  + http://hg.mozilla.org/build/buildbotcustom/
  + http://hg.mozilla.org/build/buildbot-configs/
  + http://hg.mozilla.org/build/mozharness/ <- no code examples but we will see Buildbot mention scripts from
* Purpose of walk-through:

  + expanding on :ref:`flow <from-checkin-to-tbpl>`, we are going to look at how we configure Buildbot. From monitoring changes pushed to known
    repos to assigning slaves on each of our platforms the job of compiling specified revisions of source, this walk-through will show you the core parts of our
    buildbot logic. Note this only looks at the 'compile/build' jobs we do from :ref:`TBPL` and not the test jobs.

First, let’s create a Buildbot Master:

We have scripts that will set up a machine to be a fully functioning master. They will install deps, set up environments, and link files from the above repos to
a buildbot master dir. Which links it makes depends on the master we are setting up. For example, in our production environment, we have some masters that only
deal with getting slaves to run tests on one platform like Linux. We have other masters that only schedule and prioritize which builds need to be run. There are
many more masters with specific tasks.

Rather than looking at each of these, we will be touching on a master from our staging setup. A staging master encompasses all our logic in each from our
production masters. You can think of this as the universal setup and is easier to grep while learning. In fact, you can mimic this setup on your own machine
locally. I highly recommend doing this so you can navigate the code yourself and veer off track as you get curious.

* WARNING: If you follow along with files in our repos, you will notice they are much more complex. They contain logic for handling builders and schedulers that are
  beyond our 'build a generic version of Firefox on each one of our platforms' releng 101 session. For example: we ignore all our debug, nightly, l10n, PGO,
  non-unified, no-profiling, valgrind, and xulrunner build variants.

To set up a staging master on your own machine, follow these instructions: `set up a staging local master`_

The above script will setup a virtual python environment, install Buildbot, and create a build, test, and try master all on one machine. Ignoring the 'try'
master, you can imagine the Build Master handles all the compiling/installing jobs while the Test Master handles all the tests jobs.

Let's look at the Build Master dir::

    [dev_master] jlund@Hastings163:~VIRTUAL_ENV/build-master
    > ll
    total 3176
    lrwxr-xr-x  1 jlund  staff    80B 22 Feb 21:26 staging_config.py -> /Users/jlund/devel/mozilla/dev_master/buildbot-configs/mozilla/staging_config.py
    drwxr-xr-x  6 jlund  staff   204B 22 Feb 21:26 public_html
    lrwxr-xr-x  1 jlund  staff    82B 22 Feb 21:26 project_branches.py -> /Users/jlund/devel/mozilla/dev_master/buildbot-configs/mozilla/project_branches.py
    lrwxr-xr-x  1 jlund  staff    83B 22 Feb 21:26 production_config.py -> /Users/jlund/devel/mozilla/dev_master/buildbot-configs/mozilla/production_config.py
    lrwxr-xr-x  1 jlund  staff    86B 22 Feb 21:26 preproduction_config.py -> /Users/jlund/devel/mozilla/dev_master/buildbot-configs/mozilla/preproduction_config.py
    -rw-r--r--  1 jlund  staff   753B 22 Feb 21:26 passwords.py
    lrwxr-xr-x  1 jlund  staff    20B 22 Feb 21:26 master_localconfig.py -> build_localconfig.py
    lrwxr-xr-x  1 jlund  staff    79B 22 Feb 21:26 master_common.py -> /Users/jlund/devel/mozilla/dev_master/buildbot-configs/mozilla/master_common.py
    lrwxr-xr-x  1 jlund  staff    17B 22 Feb 21:26 localconfig.py -> staging_config.py
    lrwxr-xr-x  1 jlund  staff    72B 22 Feb 21:26 config.py -> /Users/jlund/devel/mozilla/dev_master/buildbot-configs/mozilla/config.py
    lrwxr-xr-x  1 jlund  staff    81B 22 Feb 21:26 builder_master.cfg -> /Users/jlund/devel/mozilla/dev_master/buildbot-configs/mozilla/builder_master.cfg
    -rw-r--r--  1 jlund  staff   1.2K 22 Feb 21:26 buildbot.tac
    lrwxr-xr-x  1 jlund  staff    83B 22 Feb 21:26 build_localconfig.py -> /Users/jlund/devel/mozilla/dev_master/buildbot-configs/mozilla/build_localconfig.py
    -rw-r--r--  1 jlund  staff   611B 22 Feb 21:26 BuildSlaves.py
    lrwxr-xr-x  1 jlund  staff    55B 22 Feb 21:26 master.cfg -> ../buildbot-configs/mozilla/universal_master_sqlite.cfg
    -rw-r--r--  1 jlund  staff   322B 22 Feb 21:31 master_config.json
    -rw-r--r--  1 jlund  staff   224K 19 Apr 17:47 state.sqlite
    -rw-r--r--  1 jlund  staff   977K 19 Apr 17:52 twistd.log


* Note: I am not including the directories for all the 'builders' the master knows how to run or any release* b2g* thunderbird* stuff.

All Buildbot Masters have a ‘master.cfg’ file. This file's content boils down to a "BuildmasterConfig” dict that tells Buildbot everything it should do and how.
From the above dir tree output, you can see 'master.cfg' is a link to a file from one of our two Buildbot repos:
'../buildbot-configs/mozilla/universal_master_sqlite.cfg'. <- our staging master.cfg

* Navigation tip: buildbot-configs/mozilla/* represents all our Build Master logic while buildbot-configs/mozilla-tests/* holds Test Master logic.
  'buildbot-configs/mozilla2' and 'buildbot-configs/calendar' and 'buildbot-configs/seamonkey' can largely be ignored for learning purposes.

universal_master_sqlite.cfg will be our first file we look at.

First things first, let's start populating Buildmasterconfig::

    from master_common import BuildmasterConfig
    c = BuildmasterConfig

We have some items in master_localconfig that we will copy over. master_localconfig is a link to 'buildbot-configs/mozilla/build_localconfig.py'
build_localconfig will define some BuildmasterConfig items that are unique to our locally specific master setup. eg: these keys could be for what url and
port the master uses to connect with slaves. Let's grab those items::

    for key, value in master_localconfig.BuildmasterConfig.items():
        if key in c:
            c[key].extend(value)
        else:
            c[key] = value

Now let's grab the bread and butter, our main config file. 'config.py' separates all of the differences between building Mozilla products across each platform
within each `branch`_ (branch being a separate repo in most cases).

Again, it's worth noting that the config below in this circumstance will represent our Build Master's config. This is a link to
'buildbot-configs/mozilla/config.py'. That link will differ for our Test Masters but the logic flow will stay largely the same::

    from config import BRANCHES, PROJECTS

an extremely simple example of what BRANCHES will look like::

    BRANCHES = {
        'mozilla-central': {
            'some-branch-specific-item': 'foo',
            # ...
            'platforms': {
                'linux': {
                    'product_name': 'Firefox',  # the product this will be
                    'base_name': 'Linux mozilla-central',  # the buildername this will be
                    # mozharness_config will be the script the slave will run to compile/install Firefox with.
                    # This script and mozharness will be looked at later
                    'mozharness_config': {
                        'script_name': 'scripts/fx_desktop_build.py',
                        'extra_args': [
                            '--config', 'builds/releng_base_linux32_builds.py',
                        ],
                'linux64': { # contains similar values as linux as above},
                'win32': {},
                'macosx64': {},
                # ... more platforms
            },
        },
        'mozilla-aurora': {
            'platforms': {
                'win32': {},
                'linux': {},
                'linux64': {},
                'macosx64': {},
                # ... more platforms
            },
        },
        # ... more branches
    },


We will look at 'buildbot-configs/mozilla/config.py' in more detail later, but if you are curious, config.py is runnable directly outside of buildbot via
`printing config.py`_

There is also thunderbird_config and b2g_config that behave similarly and possess their own BRANCHES.

Earlier we took master_localconfig's BuildmasterConfig for specific master config items. master_localconfig also dictates which BRANCHES we will use to
install/compile against. Unlike config.py, where every branch that is known to releng resides, build_localconfig.py will dictate which branches are enabled and
which are disabled for the specific Master. build_localconfig will decide this by either its set of defaults or by referencing against a JSON file called
master_config.json. master_config.json is not inside our repos but is generated during `set up a staging local master`_. You can see it in our dir tree from
above. Let's grab the branches it considers enabled (active) so the master knows what to use::

    from master_localconfig import ACTIVE_BRANCHES, ACTIVE_PROJECTS, SLAVES

ACTIVE_BRANCHES and ACTIVE_PROJECTS are just a list of strings representing what is enabled. SLAVES is a list of dicts representing what 'slaves' this master
will know it can use at its disposal for running certain builders. Again we are only worrying about ACTIVE_BRANCHES.

We will now create an object to track all the builders, status, change_source, and schedulers that makes up our Build Master. These are the core concepts in
Buildbot that should be familiar after going over `Buildbot in 5 min`_.

This obj will be called buildObjects::

    buildObjects = {'builders': [], 'status': [], 'change_source': [], 'schedulers': []}

buildObjects is extended via generating methods. Using config.py's BRANCHES, we pass only the ones that are enabled via master_localconfig's ACTIVE_BRANCHES to
generateBranchObjects() and generateBranchObjects() will create builders, schedulers, etc based upon those BRANCHES[branch] being passed::

    for branch in ACTIVE_BRANCHES:
        branchObjects = generateBranchObjects(BRANCHES[branch], branch,
                getattr(passwords, 'secrets', None))
        buildObjects = mergeBuildObjects(buildObjects, branchObjects)

mergeBuildObjects is a glorified dict.update() that updates buildObjects as we iterate. Again note that in the full universal_master_sqlite.py, buildObjects also
takes B2G and Thunderbird items in a similar fashion.

It is worth stepping into generateBranchObjects() as it traverses through buildbot-configs and figures out the appropriate buildbot
configuration. It is imported from misc which can be found at 'buildbotcustom/misc.py'::

    def generateBranchObjects(config, name, secrets=None):
        """name is the name of branch which is usually the last part of the path
           to the repository. For example, 'mozilla-central', 'mozilla-aurora', or
           'mozilla-1.9.1'.
           config is a dictionary containing all of the necessary configuration
           information for a branch. The required keys depends greatly on what's
           enabled for a branch (unittests, xulrunner, l10n, etc). The best way
           to figure out what you need to pass is by looking at existing configs
           and using 'buildbot checkconfig' to verify.
        """
        # We return this at the end
        branchObjects = {
            'builders': [],
            'change_source': [],
            'schedulers': [],
            'status': []
        }
        # List of all the per-checkin builders
        builders = []

First let's iterate over all platforms we have enabled::

        # This section is to make it easier to disable certain products.
        # Ideally we could specify a shorter platforms key on the branch,
        # but that doesn't work
        enabled_platforms = []
        for platform in sorted(config['platforms'].keys()):
            pf = config['platforms'][platform]
            if pf['stage_product'] in config['enabled_products']:
                enabled_platforms.append(platform)

        # generate a list of builders, nightly builders (names must be different)
        # for easy access
        for platform in enabled_platforms:

            pf = config['platforms'][platform]
            builder_name = '%s build' % pf['base_name']

now we give a name to our builder based on platform and add it to a given product (eg: Firefox)::

            buildersByProduct.setdefault(
                pf['stage_product'], []).append(builder_name)

we then set up our change_source so that every time a cset is pushed to the current repo of which was passed to generateBranchObjects (eg:
config['repo_path'] == hg.m.o/projects/cedar), our schedulers we define can pick up the change and start the appropriate builds (c['builders']['the appropriate
build'])

to do this, we use :ref:`HgPoller` mentioned in :ref:`flow <from-checkin-to-tbpl>`::

            branchObjects['change_source'].append(HgPoller(
                hgURL=config['hgurl'],
                branch=config.get("poll_repo", config['repo_path']),
                tipsOnly=tipsOnly,
                maxChanges=maxChanges,
                repo_branch=repo_branch,
                pollInterval=pollInterval,
            ))

time for the schedulers! Here we are basically saying when there is a push to the repo matching the Scheduler()'s 'branch', trigger all the builders with
the names from the Scheduler's 'builderNames'::

            # schedulers
            # this one gets triggered by the HG Poller
            for product, product_builders in buildersByProduct.items():
                branchObjects['schedulers'].append(Scheduler(
                    name=scheduler_name_prefix + "-" + product,
                    branch=config.get("poll_repo", config['repo_path']),
                    builderNames=product_builders,
                    fileIsImportant=fileIsImportant,
                    **extra_args
                ))

note - check here for more on our :ref:`buildbot schedulers`.

last but not least, the 'builders'. Above we defined the names (strings) of the builders. Now we will create actual buildbot builders that are associated with
those names so the schedulers will actually have a builder to call::

            for platform in enabled_platforms:
                branchObjects['builders'].extend(
                    generateDesktopMozharnessBuilders(
                        name, platform, config
                    )
                )
            return branchObjects

we can briefly look at generateDesktopMozharnessBuilders::

    def generateDesktopMozharnessBuilders(name, platform, config):
        desktop_mh_builders = []

        pf = config['platforms'][platform]

if you recall above when we gave a crude example of what BRANCHES from buildbot-configs/mozilla/config.py would look like, we defined a mozharness_config at the
platform level. Below we use that to define what our builder does::

        base_extra_args = pf['mozharness_config'].get('extra_args', [])
        # let's grab the extra args that are defined at misc level
        branch_and_pool_args = []
        branch_and_pool_args.extend(['--branch', name])
        if config.get('staging'):
            branch_and_pool_args.extend(['--build-pool', 'staging'])
        else:  # this is production
            branch_and_pool_args.extend(['--build-pool', 'production'])
        base_extra_args.extend(branch_and_pool_args)
        base_builder_dir = '%s-%s' % (name, platform)

Buildbot Builders are made up of a series of cmds (build steps). That series (a factory) is associated with a Builder. So you can think of a Builder as
something with a name that is a string that cooresponds with a buildername from a scheduler, a factory, and some other important data like what slaves are
capable of running the respective builder.

let's look at the factory::

        factory = makeMHFactory(config, pf, signingServers=dep_signing_servers,
                                extra_args=base_extra_args)

            # and our factory creating method
            def makeMHFactory(config, pf, extra_args=None, **kwargs):
                factory_class = ScriptFactory
                mh_cfg = pf['mozharness_config']

                scriptRepo = config.get('mozharness_repo_url',
                                        '%s%s' % (config['hgurl'], config['mozharness_repo_path']))
                factory = factory_class(
                    scriptRepo=scriptRepo,
                    interpreter=mh_cfg.get('mozharness_python'),
                    scriptName=mh_cfg['script_name'],
                    reboot_command=mh_cfg.get('reboot_command'),
                    extra_args=extra_args,
                    script_timeout=pf.get('timeout', 3600),
                    script_maxtime=pf.get('maxTime', 4 * 3600),
                    **kwargs
                )
                return factory

For our factory, we use the ScriptFactory class to set out a few setup cmds, the main script we want to call, and then some tear down cmds. Remember
cmds being BuildSteps in Buildbot world.

Let's look at a snippet of ScriptFactory Quickly. You can find it where we keep other factories: buildbotcustom/process/factory.py

Remember factories encapsulate a series of pre-defined cmds that a buildbot master will tell a buildbot slave to run sequentially, once a change_source (cset
lands on a repo), triggers a scheduler to trigger a builder with that factory::

    class ScriptFactory(RequestSortingBuildFactory):

        def __init__(self, scriptRepo, scriptName, cwd=None, interpreter=None):
            BuildFactory.__init__(self)
            self.platform = platform
            self.env = env.copy()
            self.cmd = [scriptName]

            if extra_args:
                self.cmd.extend(extra_args)

we set some initial steps like the basedir that we will run commands and work from on the slave::

            self.addStep(SetProperty(
                name='get_basedir',
                property='basedir',
                command=self.get_basedir_cmd,
                workdir='.',
                haltOnFailure=True,
            ))

then we will need to tell the slave to clone the repo that is home to the script we are going to get the slave to call (in this case it will be cloning
Mozharness)::

            self.addStep(MercurialCloneCommand(
                name="clone_scripts",
                command=[hg_bin, 'clone', scriptRepo, 'scripts'],
                workdir=".",
                haltOnFailure=True,
                retry=False,
                log_eval_func=rc_eval_func({0: SUCCESS, None: RETRY}),
            ))
            self.runScript()
            self.addCleanupSteps()
            self.reboot()

then we define how the script will be called by the slave::

        def runScript(self):
            self.preRunScript()
            self.addStep(MockCommand(
                name="run_script",
                command=self.cmd,
                env=self.env,
                timeout=self.script_timeout,
                maxTime=self.script_maxtime,
                log_eval_func=self.log_eval_func,
                workdir=".",
                haltOnFailure=True,
                warnOnWarnings=True,
                mock=self.use_mock,
                target=self.mock_target,
            ))

finally we tell the slave to reboot itself::

        def reboot(self):
            self.addStep(DisconnectStep(
                name='reboot',
                flunkOnFailure=False,
                warnOnFailure=False,
                alwaysRun=True,
                workdir='.',
                description="reboot",
                command=self.reboot_command,
                force_disconnect=do_disconnect,
                env=self.env,
            ))

and that's it for the factory and list of cmds. We pass that factory to the builder we are defining and that builder gets extended to buildObjects['builders']::

        generic_builder = {
            'name': '%s build' % pf['base_name'],
            'builddir': base_builder_dir,
            'slavebuilddir': normalizeName(base_builder_dir),
            'slavenames': pf['slaves'],
            'nextSlave': next_slave,
            'factory': factory,
            'category': name,
            'properties': mh_build_properties.copy(),
        }
        desktop_mh_builders.append(generic_builder)

        # finally let's return which builders we did so we know what's left to do!
        return desktop_mh_builders

We have reached the end of misc.py's generateBranchObjects()

Back in our universal_master_sqlite.py, we finish up with adding logic to how we define the steps to run after a job completes. This will contain logic to
parsing if the job was a success, failure, etc and also concat the job's steps into one log that is uploaded and fed to TBPL. These post run steps are explained
in :ref:`postrun.py`. Notice we add this to our `status`_ key

Here we also mention our QueueDir objs. To understand that, see `queue directories`_::

    # Create our QueueDir objects
    # This is reloaded in buildbotcustom.misc
    from mozilla_buildtools.queuedir import QueueDir
    commandsQueue = QueueDir('commands', '%s/commands' % master_localconfig.QUEUEDIR)
    from buildbotcustom.status.queued_command import QueuedCommandHandler
    buildObjects['status'].append(QueuedCommandHandler(
        command=[sys.executable, os.path.join(os.path.dirname(buildbotcustom.__file__), 'bin', 'postrun.py'), '-c', os.path.abspath(os.path.join(os.curdir, 'postrun.cfg'))],
        queuedir=commandsQueue,
    ))

We can finish up by extending our BuildmasterConfig with all the 'builders' 'status' 'change_source' and 'schedulers' we generated from generateBranchObjects()::

    c['builders'].extend(buildObjects['builders'])
    c['status'].extend(buildObjects['status'])
    c['change_source'].extend(buildObjects['change_source'])
    c['schedulers'].extend(buildObjects['schedulers'])

Phew! That's the end of that file. We can consider Buildbot to be 'configured'. All that is left to do is to start a Buildbot Master with this configuration on a machine and connect Buildbot Slaves to it.

You might be thinking "wait, I still haven't seen any of our logic for actually 'compiling' Firefox from source."

And that's true! Up to this point, we have only gone over the logic from 'a user checking in a cset' to 'a buildbot master triggering build jobs on a slave
from each of our platforms.'. Everything involved on with how to build firefox (the script we defined in ScriptFactory) we have yet to see. But
that is for walk-through 2: :ref:`Building Firefox in automation`

Recap -- the full code from examples above
------------------------------------------

buildbot-configs/mozilla/universal_master_sqlite.cfg::

    from master_common import BuildmasterConfig
    c = BuildmasterConfig

    for key, value in master_localconfig.BuildmasterConfig.items():
        if key in c:
            c[key].extend(value)
        else:
            c[key] = value

    # Create our QueueDir objects
    # This is reloaded in buildbotcustom.misc
    from mozilla_buildtools.queuedir import QueueDir
    commandsQueue = QueueDir('commands', '%s/commands' % master_localconfig.QUEUEDIR)
    from buildbotcustom.status.queued_command import QueuedCommandHandler
    c['status'].append(QueuedCommandHandler(
        command=[sys.executable, os.path.join(os.path.dirname(buildbotcustom.__file__), 'bin', 'postrun.py'), '-c', os.path.abspath(os.path.join(os.curdir, 'postrun.cfg'))],
        queuedir=commandsQueue,
    ))

    from config import BRANCHES, PROJECTS

    from master_localconfig import ACTIVE_BRANCHES, ACTIVE_PROJECTS, SLAVES

    buildObjects = {'builders': [], 'status': [], 'change_source': [], 'schedulers': []}

    for branch in ACTIVE_BRANCHES:
        branchObjects = generateBranchObjects(BRANCHES[branch], branch,
                getattr(passwords, 'secrets', None))
        buildObjects = mergeBuildObjects(buildObjects, branchObjects)

    c['builders'].extend(buildObjects['builders'])
    c['status'].extend(buildObjects['status'])
    c['change_source'].extend(buildObjects['change_source'])
    c['schedulers'].extend(buildObjects['schedulers'])

buildbotcustom/misc.py::

    def generateBranchObjects(config, name, secrets=None):
        """name is the name of branch which is usually the last part of the path
           to the repository. For example, 'mozilla-central', 'mozilla-aurora', or
           'mozilla-1.9.1'.
           config is a dictionary containing all of the necessary configuration
           information for a branch. The required keys depends greatly on what's
           enabled for a branch (unittests, xulrunner, l10n, etc). The best way
           to figure out what you need to pass is by looking at existing configs
           and using 'buildbot checkconfig' to verify.
        """
        # We return this at the end
        branchObjects = {
            'builders': [],
            'change_source': [],
            'schedulers': [],
            'status': []
        }
        # List of all the per-checkin builders
        builders = []

        # This section is to make it easier to disable certain products.
        # Ideally we could specify a shorter platforms key on the branch,
        # but that doesn't work
        enabled_platforms = []
        for platform in sorted(config['platforms'].keys()):
            pf = config['platforms'][platform]
            if pf['stage_product'] in config['enabled_products']:
                enabled_platforms.append(platform)

        # generate a list of builders, nightly builders (names must be different)
        # for easy access
        for platform in enabled_platforms:

            pf = config['platforms'][platform]
            builder_name = '%s build' % pf['base_name']

            buildersByProduct.setdefault(
                pf['stage_product'], []).append(builder_name)

            branchObjects['change_source'].append(HgPoller(
                hgURL=config['hgurl'],
                branch=config.get("poll_repo", config['repo_path']),
                tipsOnly=tipsOnly,
                maxChanges=maxChanges,
                repo_branch=repo_branch,
                pollInterval=pollInterval,
            ))

            # schedulers
            # this one gets triggered by the HG Poller
            for product, product_builders in buildersByProduct.items():
                branchObjects['schedulers'].append(scheduler_class(
                    name=scheduler_name_prefix + "-" + product,
                    branch=config.get("poll_repo", config['repo_path']),
                    builderNames=product_builders,
                    fileIsImportant=fileIsImportant,
                    **extra_args
                ))

            for platform in enabled_platforms:
                # shorthand
                pf = config['platforms'][platform]
                branchObjects['builders'].extend(
                    generateDesktopMozharnessBuilders(
                        name, platform, config
                    )
                )
            return branchObjects

    def generateDesktopMozharnessBuilders(name, platform, config):
        desktop_mh_builders = []

        pf = config['platforms'][platform]

        base_extra_args = pf['mozharness_config'].get('extra_args', [])
        # let's grab the extra args that are defined at misc level
        branch_and_pool_args = []
        branch_and_pool_args.extend(['--branch', name])
        if config.get('staging'):
            branch_and_pool_args.extend(['--build-pool', 'staging'])
        else:  # this is production
            branch_and_pool_args.extend(['--build-pool', 'production'])
        base_extra_args.extend(branch_and_pool_args)
        base_builder_dir = '%s-%s' % (name, platform)

        factory = makeMHFactory(config, pf, signingServers=dep_signing_servers,
                                extra_args=base_extra_args)
        generic_builder = {
            'name': '%s build' % pf['base_name'],
            'builddir': base_builder_dir,
            'slavebuilddir': normalizeName(base_builder_dir),
            'slavenames': pf['slaves'],
            'nextSlave': next_slave,
            'factory': factory,
            'category': name,
            'properties': mh_build_properties.copy(),
        }
        desktop_mh_builders.append(generic_builder)

        # finally let's return which builders we did so we know what's left to do!
        return desktop_mh_builders


        # and our factory creating method
        def makeMHFactory(config, pf, extra_args=None, **kwargs):
            factory_class = ScriptFactory
            mh_cfg = pf['mozharness_config']

            scriptRepo = config.get('mozharness_repo_url',
                                    '%s%s' % (config['hgurl'], config['mozharness_repo_path']))
            factory = factory_class(
                scriptRepo=scriptRepo,
                interpreter=mh_cfg.get('mozharness_python'),
                scriptName=mh_cfg['script_name'],
                reboot_command=mh_cfg.get('reboot_command'),
                extra_args=extra_args,
                script_timeout=pf.get('timeout', 3600),
                script_maxtime=pf.get('maxTime', 4 * 3600),
                **kwargs
            )
            return factory

buildbotcustom/process/factory.py::

    class ScriptFactory(RequestSortingBuildFactory):

        def __init__(self, scriptRepo, scriptName, cwd=None, interpreter=None):
            BuildFactory.__init__(self)
            self.platform = platform
            self.env = env.copy()
            self.cmd = [scriptName]

            if extra_args:
                self.cmd.extend(extra_args)

            self.addStep(SetProperty(
                name='get_basedir',
                property='basedir',
                command=self.get_basedir_cmd,
                workdir='.',
                haltOnFailure=True,
            ))

            self.addStep(MercurialCloneCommand(
                name="clone_scripts",
                command=[hg_bin, 'clone', scriptRepo, 'scripts'],
                workdir=".",
                haltOnFailure=True,
                retry=False,
                log_eval_func=rc_eval_func({0: SUCCESS, None: RETRY}),
            ))
            self.runScript()
            self.addCleanupSteps()
            self.reboot()

        def runScript(self):
            self.preRunScript()
            self.addStep(MockCommand(
                name="run_script",
                command=self.cmd,
                env=self.env,
                timeout=self.script_timeout,
                maxTime=self.script_maxtime,
                log_eval_func=self.log_eval_func,
                workdir=".",
                haltOnFailure=True,
                warnOnWarnings=True,
                mock=self.use_mock,
                target=self.mock_target,
            ))

        def reboot(self):
            self.addStep(DisconnectStep(
                name='reboot',
                flunkOnFailure=False,
                warnOnFailure=False,
                alwaysRun=True,
                workdir='.',
                description="reboot",
                command=self.reboot_command,
                force_disconnect=do_disconnect,
                env=self.env,
            ))


.. _Buildbot Docs: http://docs.buildbot.net
.. _Buildbot in 5 min: http://docs.buildbot.net/current/tutorial/fiveminutes.html
.. _set up a staging local master: https://wiki.mozilla.org/ReleaseEngineering/How_To/Setup_Personal_Development_Master#Setup.2FRunning_local_master_scheduler_on_laptop_-_not_dev-master
.. _queue directories: https://wiki.mozilla.org/ReleaseEngineering/Queue_directories
.. _status: http://docs.buildbot.net/current/tutorial/fiveminutes.html#status-targets
.. _printing config.py: https://wiki.mozilla.org/ReleaseEngineering:TestingTechniques#config.py_is_executable.21
.. _branch: https://wiki.mozilla.org/Releases/Branches
