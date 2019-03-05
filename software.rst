.. _software:

Software
========

.. _taskcluster:

Taskcluster
-----------

Taskcluster Overview
~~~~~~~~~~~~~~~~~~~~

We need to flesh this out.

- `Taskcluster docs`_
- `Gecko in-tree taskcluster docs`_

.. _Taskcluster docs: https://docs.taskcluster.net
.. _Gecko in-tree taskcluster docs: https://firefox-source-docs.mozilla.org/taskcluster/taskcluster/index.html

hg pushlog
----------
Mozilla maintains a record of when changes are pushed into various
repositories on `hg.mozilla.org`_.

The pushlog has several interfaces of interest, the html view which is
useful to developers, and the json format which is more useful for
automated systems.

.. _pushlog.py hook: http://hg.mozilla.org/hgcustom/hghooks/file/15e5831ab26b/mozhghooks/pushlog.py
.. _hg.mozilla.org: https://hg.mozilla.org

Mozharness
----------

Mozharness is a configuration driven script harness. It is a Script harness in that it knows
how to automate a set of tasks. The scripts tend to not to need to know if you are running on Windows or
Linux, nor does it know much about what tests or commands you need to run. The scripts get those
varying details from a corresponding config (hence it being driven by configuration).

Let's take a more concrete example of why you might use Mozharness. Let's say you have a new
test suite that you want to start running against every new checkin of Firefox
desktop across our continous integration for our various repositories.
You know at a high level you need to do a number of things each time you run the tests:

    1. Clear a work space so you are starting off fresh
    2. Clone some repository that provides you with the tests you are going to call
    3. Download a binary of Firefox to test against
    4. The tests are in python and have some dependencies so you need to create a virtualenv and install some modules
    5. Run the tests against the binary
    6. Parse the output and interpret the return code
    7. Log the results and and report some sort of overall status

Doing this for 10.8 OS X with mozilla-central in your local machine and with known static
paths/packages might be pretty straight forward, however, this becomes a bit more complicated
when you need to support X different platforms, over a dozen repositories, and a varying set of
build types (e.g. pgo, debug, asan, etc).

Supporting all those variants can quickly make a script harness turn into a bag of snakes. I am
going to prove this by creating a new script for Mozharness which can simplify this and, through
the process, provide an outline of the core modules of mozharness and how you might go about creating or
adding to an existing script for your own needs. I encourage you to follow along and identify the
core concepts with some mozharness coding.

The official repository location: https://hg.mozilla.org/mozilla-central/file/default/testing/mozharness

The File Structure::

    |-- configs -> where all config files live that are used against individual scripts
    |-- docs
    |-- examples
    |-- external_tools
    |-- mozfile
    |-- mozharness
    |   |-- base -> the core of mozharness and common tools for extending scripts
    |   `-- mozilla -> common tools for extending scripts that are specific to Mozilla's needs
    |-- mozinfo
    |-- mozprocess
    |-- scripts -> where all the callable scripts go
    `-- test


Before we get to the scripts, I'd like to cover three classes that each correspond to a
critical part of Mozharness:

     BaseLogger -> mozharness/base/log.py

     BaseConfig -> mozharness/base/config.py

     BaseScript -> mozharness/base/script.py

BaseLogger
~~~~~~~~~~

BaseLogger provides a consistent logging for script runs::

    13:13:19     INFO - #####
    13:13:19     INFO - ##### Running clobber step.
    13:13:19     INFO - #####
    13:13:19     INFO - Running main action method: clobber
    13:13:19     INFO - retry: Calling <bound method FxDesktopBuild.run_command of <__main__.FxDesktopBuild object at 0x23c38d0>> with args: [['/builds/slave/ash-l64-0000000000000000000000/scripts/external_tools/clobberer.py', '-s', 'scripts', '-s', 'logs', '-s', 'buildprops.json', '-s', 'token', '-t', '168', 'http://clobberer.pvt.build.mozilla.org/index.php', u'ash', u'Linux x86-64 ash build', 'ash-l64-0000000000000000000000', u'b-linux64-ix-0002', u'http://buildbot-master84.srv.releng.scl3.mozilla.com:8001/']], kwargs: {'error_list': [{'substr': 'Error contacting server', 'explanation': 'Error contacting server for clobberer information.', 'level': 'error'}], 'cwd': '/builds/slave'}, attempt #1
    13:13:19     INFO - Running command: ['/builds/slave/ash-l64-0000000000000000000000/scripts/external_tools/clobberer.py', '-s', 'scripts', '-s', 'logs', '-s', 'buildprops.json', '-s', 'token', '-t', '168', 'http://clobberer.pvt.build.mozilla.org/index.php', u'ash', u'Linux x86-64 ash build', 'ash-l64-0000000000000000000000', u'b-linux64-ix-0002', u'http://buildbot-master84.srv.releng.scl3.mozilla.com:8001/'] in /builds/slave
    13:13:19     INFO - Copy/paste: /builds/slave/ash-l64-0000000000000000000000/scripts/external_tools/clobberer.py -s scripts -s logs -s buildprops.json -s token -t 168 http://clobberer.pvt.build.mozilla.org/index.php ash "Linux x86-64 ash build" ash-l64-0000000000000000000000 b-linux64-ix-0002 http://buildbot-master84.srv.releng.scl3.mozilla.com:8001/
    13:13:22     INFO -  Checking clobber URL: http://clobberer.pvt.build.mozilla.org/index.php
    13:13:22     ERROR - can not reach clobber URL
    13:13:22     INFO -  b2g_b2g-in_ham_dep-00000000000:Our last clobber date:  None

We always start with a timestamp and then a log level for each line. Log levels, by default,
are debug, info, warning, error, critical, and fatal. Logs are outputted via BaseLogger.log_message()

I am going to show you a snippet of code from the BaseLogger only to show you what happens under
the hood, This class is rarely directly reached by Mozharness scripts.

snippet of BaseLogger mozharness/base/log.py::

    class BaseLogger(object):
        """Create a base logging class.
        LEVELS = {
            DEBUG: logging.DEBUG,
            INFO: logging.INFO,
            WARNING: logging.WARNING,
            ERROR: logging.ERROR,
            CRITICAL: logging.CRITICAL,
            FATAL: FATAL_LEVEL
        }

        def __init__(
            self, log_level=INFO,
            log_format='%(message)s',
            log_date_format='%H:%M:%S',
            log_name='test',
            log_to_console=True,
            log_dir='.',
            log_to_raw=False,
            logger_name='',
            append_to_log=False,
        ):

            self.all_handlers = []
            self.log_files = {}

            self.create_log_dir()

        def create_log_dir(self):
            if os.path.exists(self.log_dir):
                if not os.path.isdir(self.log_dir):
                    os.remove(self.log_dir)
            if not os.path.exists(self.log_dir):
                os.makedirs(self.log_dir)
            self.abs_log_dir = os.path.abspath(self.log_dir)

        def new_logger(self, logger_name):
            """Create a new logger.
            By default there are no handlers.
            """
            self.logger = logging.getLogger(logger_name)
            self.logger.setLevel(self.get_logger_level())
            self._clear_handlers()
            if self.log_to_console:
                self.add_console_handler()
            if self.log_to_raw:
                self.log_files['raw'] = '%s_raw.log' % self.log_name
                self.add_file_handler(os.path.join(self.abs_log_dir,
                                                   self.log_files['raw']),
                                      log_format='%(message)s')

        def log_message(self, message, level=INFO, exit_code=-1, post_fatal_callback=None):
            if level == IGNORE:
                return
            for line in message.splitlines():
                self.logger.log(self.get_logger_level(level), line)
            if level == FATAL:
                if callable(post_fatal_callback):
                    self.logger.log(FATAL_LEVEL, "Running post_fatal callback...")
                    post_fatal_callback(message=message, exit_code=exit_code)
                self.logger.log(FATAL_LEVEL, 'Exiting %d' % exit_code)
                raise SystemExit(exit_code)

So how do we avail of this if we don't call methods from it? LogMixin class provides helper methods
for things like log(msg, level) or, even simpler, self.{level}(msg) as in: self.info(msg) or
self.error(msg) and BaseLogger inherits those methods. These are the ones you will likely use the most.

* A note about self.fatal(msg) or self.log(msg, FATAL): these methods will also cause the script to halt and exit

snippet of LogMixin mozharness/base/log.py::

    class LogMixin(object):

        def log(self, message, level=INFO, exit_code=-1):
            if self.log_obj:
                return self.log_obj.log_message(
                    message, level=level,
                    exit_code=exit_code,
                    post_fatal_callback=self._post_fatal,
                )
            if level == INFO:
                if self._log_level_at_least(level):
                    self._print(message)
            elif level == DEBUG:
                if self._log_level_at_least(level):
                    self._print('DEBUG: %s' % message)
            elif level in (WARNING, ERROR, CRITICAL):
                if self._log_level_at_least(level):
                    self._print("%s: %s" % (level.upper(), message), stderr=True)
            elif level == FATAL:
                if self._log_level_at_least(level):
                    self._print("FATAL: %s" % message, stderr=True)
                raise SystemExit(exit_code)

        def debug(self, message):
            self.log(message, level=DEBUG)

        def info(self, message):
            self.log(message, level=INFO)

        def warning(self, message):
            self.log(message, level=WARNING)

        # ... etc

One  final thing worth mentioning here is that mozharness can also save a single log file,
or even split your log into multiple log files based on individual log levels. Since splitting the
log into multiple files is the most common, I'll mention how that works. MultiFileLogger is a
subclass of BaseLogger and does this work for you. The split logic will take a script run and save
the following::

    logs/ -> default log path unless you overwrite it
        log_info.log -> contains every single line of output
        log_warning.log -> contains only warning and worse (error, crit, fatal) lines of output
        log_error.log -> contains only error and worse...
        log_critical.log -> ... and so on
        log_fatal.log

So how do you add logging to your script? Adding the logging module to your script is already done
for you if you avail of BaseScript (you pretty much always will want to). BaseScript connects all
core parts of Mozharness and we will dive into that shortly.

BaseConfig
~~~~~~~~~~

This is the class that will interpret all of your configuration from many different sources. These
sources could be CLI arguments, json or python (dict) files, remote url files,
or a static configuration (dict) inputted directly from the script.

BaseConfig provides a constant hierarchy across your scripts so if you have multiple duplicate
keys from various sources, a precedence will decide what you end up with.

 * the hierarchy from highest to lowest: CLI options -> config files -> static from script

Not sure what to put in a config file or how to extend CLI options? Don't worry,
we will be doing a full example shortly.

After BaseConfig constructs what your config will ultimately look like against a given script run, it
will lock the items so it becomes an immutable dict. This expresses how a config is what drives the
job, not the script. It is essentially read only dict so feel free to use config[key] and
config.get(key, default) syntax.

Finally, BaseConfig also interprets what Actions (steps of  the job)  that will be run. Defining
and understanding actions will be explained in the BaseScript section.


snippet of BaseConfig mozharness/base/config.py::

     class BaseConfig(object):
        """Basic config setting/getting.
        """
        def __init__(self, config=None, initial_config_file=None, config_options=None,
                     all_actions=None, default_actions=None,
                     volatile_config=None, option_args=None,
                     require_config_file=False, usage="usage: %prog [options]"):
            # ...
            # ...
            if initial_config_file:
                initial_config = parse_config_file(initial_config_file)
                self.all_cfg_files_and_dicts.append(
                    (initial_config_file, initial_config)
                )
                self.set_config(initial_config)
            if config_options is None:
                config_options = []
            # CREATES AN OPTION PARSER FOR OUR cli ARGS
            self._create_config_parser(config_options, usage)
            # PARSE THE ARGS THAT WERE GIVEN FOR THE CURRENT SCRIPT CALL
            # AND INTERPRET ANY CONFIG FILES USED
            self.parse_args(args=option_args)

        def get_read_only_config(self):
            return ReadOnlyDict(self._config)

        def _create_config_parser(self, config_options, usage):
            self.config_parser = ExtendedOptionParser(usage=usage)
            self.config_parser.add_option(
                "--work-dir", action="store", dest="work_dir",
                type="string", default="build",
                help="Specify the work_dir (subdir of base_work_dir)"
            )
            # ...
            # ... more default options for your scripts
            # ...

        def parse_args(self, args=None):
            self.command_line = ' '.join(sys.argv)
            if not args:
                args = sys.argv[1:]
            (options, args) = self.config_parser.parse_args(args)

            defaults = self.config_parser.defaults.copy()

            if not options.config_files:
                # SOMETIMES WE DON'T ALWAYS NEED A CONFIG FILE
                if self.require_config_file:
                    # BUT WE CAN FORCE THE REQUIREMENT TO HAVE ONE
                    if options.list_actions:
                        self.list_actions()
                    print("Required config file not set! (use --config-file option)")
                    raise SystemExit(-1)
            else:
                # INTERPRET THE CONFIG FILE(S) AND THEN ADDD THAT TO SELF.CONFIG
                self.all_cfg_files_and_dicts.extend(self.get_cfgs_from_files(
                    # append opt_config to allow them to overwrite previous configs
                    options.config_files + options.opt_config_files, parser=options
                ))
                config = {}
                for i, (c_file, c_dict) in enumerate(self.all_cfg_files_and_dicts):
                    config.update(c_dict)
                self.set_config(config)
            # MAKE SURE THAT DEFAULT OPTIONS ARE OVERRIDDEN BY CONFIG FILE OPTIONS AND PARSER OPTIONS
            for key in defaults.keys():
                value = getattr(options, key)
                if value is None:
                    continue
                # Don't override config_file defaults with config_parser defaults
                if key in defaults and value == defaults[key] and key in self._config:
                    continue
                self._config[key] = value

            # ...
            # ...
            # determine action details from configuration. more on that later
            # ...
            # ...

            self.options = options
            self.args = args
            return (self.options, self.args)

Like BaseLogger, BaseScript will instantiate BaseConfig and attach itself as an attr so you won't
have to call BaseConfig directly.

* Wondering what your config will look like if you only inherit from BaseScript and don't extend your script with any CLI or config files::

     # defaults
     {'append_to_log': False,  # whether you want to start your log files cleanly or append to prev run
      'base_work_dir': '~/devel/mozilla/dirtyRepos/mozharness_jlund', # path you call the script from
      'log_level': 'info',  # what default level you want to start at
      'log_to_console': True,
      'opt_config_files': (), # a list of config files passed for the run
      'volatile_config': {'actions': None, 'add_actions': None, 'no_actions': None},
      # used by BaseConfig to determine what actions to run
      'work_dir': 'build' # the dirname of where you will put and run things. e.g. downloads/src/artifacts
      }


BaseScript
~~~~~~~~~~

You may have an idea now that BaseScript is where everything comes together. By inheriting and
instantiating BaseScript, you get your logging obj (self.log_obj),
your configuration (self.config), and your actions used for the script (self.actions).  You
should be familiar about logging and configuration so let's discuss actions.

Actions express the list of steps for a job on a given run. Think 'remove tree',
'clone something', 'run this test suite', 'clean up'. Essetially self.actions is a list:

     ['clobber', 'clone', 'run-tests', 'clean-up']

What happens is when you call BaseScript.run_and_exit(), Mozharness will run through each action in
the list and look for a corresponding method within scope of your script class. e.g. when we get to
the 'clone' action in self.actions, BaseScript will look for self.clone() and execute that method.

* note about actions names: when the action name uses a hyphen, e.g. 'run-tests', BaseScript will replace the '-' with a '_' so it will look for self.run_tests().

In addition to running actions, BaseScript also has an overall status: self.return_code. This value
can be manipulated as the script runs so you can keep track of how your script did if you do not
want to halt early or the overall return value is swallowed downstream.

BaseScript has a few 'helper' methods itself but it leverages from one of the more powerful
Mixins in Mozharness: BaseMixin. BaseMixin is aimed to provide you with a set of
tools for doing common tasks: e.g. sys admin, networking, subprocess commands. It does so but
aims to be platform agnostic while incorporating Mozharness's self.log_obj and self.config.

BaseScript mozharness/base/script.py::

    class BaseScript(ScriptMixin, LogMixin, object):
        def __init__(self, config_options=None, ConfigClass=BaseConfig,
                     default_log_level="info", **kwargs):
            super(BaseScript, self).__init__()

            self.return_code = 0
            # HERE IS WHERE WE INSTANTIATE THE CONFIG (99% OF THE TIME bASEcONFIG)
            rw_config = ConfigClass(config_options=config_options, **kwargs)
            self.config = rw_config.get_read_only_config()
            # WE DERIVE OUR LIST OF ACTIONS WE WANT TO USE FOR SCRIPT CALL
            self.actions = tuple(rw_config.actions)
            # here is where we create our log_obj (a subclass of BaseLogger)
            self.log_obj = None
            self.new_log_obj(default_log_level=default_log_level)

            # ADD A DECORATOR METHOD THAT WE CAN USE IN OUR SCRIPT IF WE WANT TO CHANGE
            # SELF.CONFIG BEFORE LOCKING IT FOR GOOD
            self._pre_config_lock(rw_config)
            # SET SELF.CONFIG TO READ-ONLY.
            self._config_lock()

        def run_and_exit(self):
            """Runs the script and exits the current interpreter."""
            sys.exit(self.run())

        def run(self):
            # VERY SIMPLIFIED
            try:
                for action in self.all_actions:
                    self.run_action(action)
            except Exception:
                self.fatal("Uncaught exception: %s" % traceback.format_exc())
            if self.config.get("copy_logs_post_run", True):
                self.copy_logs_to_upload_dir()

            return self.return_code

        def run_action(self, action):
            # AGAIN SIMPLIFIED DRAMATICALLY
            if action not in self.actions:
                self.action_message("Skipping %s step." % action)
                return

            method_name = action.replace("-", "_")
            try:
                self._possibly_run_method(method_name, error_if_missing=True)

Mozharness Example
~~~~~~~~~~~~~~~~~~

Before we dive into the example, I'd like to outline some common built in CLI args you can use to
explore the concepts mentioned above:

With any script, you can run --help to see a list of options you can pass:

for modifying/listing self.config::

  --work-dir=WORK_DIR   Specify the work_dir (subdir of base_work_dir)
  --base-work-dir=BASE_WORK_DIR
                        Specify the absolute path of the parent of the working
                        directory
  -c CONFIG_FILES, --config-file=CONFIG_FILES, --cfg=CONFIG_FILES
                        Specify the config files
  -C OPT_CONFIG_FILES, --opt-config-file=OPT_CONFIG_FILES, --opt-cfg=OPT_CONFIG_FILES
                        Specify the optional config files
  --dump-config         List and dump the config generated from this run to a
                        JSON file.
  --dump-config-hierarchy
                        Like dump config but will list and dump which config
                        files were used making up the config and specify their
                        own keys/values that were not overwritten by another
                        cfg -- held the highest hierarchy.

for modifying self.log_obj::

    --log-level=LOG_LEVEL
                        Set log level
                        (debug|info|warning|error|critical|fatal)
    -q, --quiet         Don't log to the console
    --append-to-log     Append to the log
    --multi-log         Log using MultiFileLogger
    --simple-log        Log using SimpleFileLogger

for modifying/listing self.actions::

    --list-actions      List all available actions, then exit
    --add-action=ACTIONS
                        Add action ['clobber', 'nap', 'ship-it'] to the list
                        of actions
    --no-action=ACTIONS
                        Don't perform action
    --{action}          for any action the script knows about, pass it explicitly and the script
                        will only run that action

* pro learning tip: use --list-actions --dump-config and --dump-config-hierarchy

They are all great ways of interpreting what actions will be called or what self.config will look
like based on the options and config files passed to a script run. Running any one of those three
against a script + other options won't cause any actions to be run so they are not dangerous.

Ok, so how can we put all these concepts together in some trivial script? Lucky for us,
there is already a committed example we can use in the mozharness repo

ActionsConfigExample examples/action_config_script.py::

    sys.path.insert(1, os.path.dirname(sys.path[0]))
    # MESSING WITH SYS.PATH LIKE ABOVE IS A NORMAL IDIOM SO WE CAN REACH MOZHARNESS/* BELOW
    from mozharness.base.script import BaseScript


    # ActionsConfigExample {{{1
    class ActionsConfigExample(BaseScript):  # HERE IS WHERE WE INHERIT BASESCRIPT INTO OUR CLASS
        config_options = [[  # WE ADD SOME OF OUR OWN OPTIONS IN ADDITION TO WHAT WE GET FROM DEFAULT
            ['--beverage', ],
            {"action": "store",
             "dest": "beverage",
             "type": "string",
             "help": "Specify your beverage of choice",
             }
        ], [
            ['--ship-style', ],
            {"action": "store",
             "dest": "ship_style",
             "type": "choice",
             "choices": ["1", "2", "3"],
             "help": "Specify the type of ship",
             }
        ], [
            ['--long-sleep-time', ],
            {"action": "store",
             "dest": "long_sleep_time",
             "type": "int",
             "help": "Specify how long to sleep",
             }
        ]]

        def __init__(self, require_config_file=False):
            # OUR ActionsConfigExample MERELY INSTANTIATES BaseScripts __init__
            super(ActionsConfigExample, self).__init__(
                config_options=self.config_options,  # PASS IN THE ADDITIONAL CLI OPTIONS
                # THESE ARE ALL THE ACTIONS THAT ARE POSSIBLE TO RUN. BaseScript WILL VERIFY IT
                # CAN SEE A METHOD FOR EACH OF THESE
                all_actions=[
                    'clobber',
                    'nap',
                    'ship-it',
                ],
                # IF WE DON'T SPECIFY WHICH ACTIONS TO RUN IN A CONFIG OR CLI, DO THESE DEFAULT ONES
                default_actions=[
                    'clobber',
                    'nap',
                    'ship-it',
                ],
                # IF YOUR SCRIPT REQUIRES A CONFIG FILE, YOU CAN USE REQUIRE_CONFIG_FILE
                require_config_file=require_config_file,
                # this is our default config (what will be added to self.config)
                # remember keys from config files will take precedence over these defaults
                # CLI options like the cooresponding --beverage will take precendence over all
                config={
                    'beverage': "kool-aid",
                    'long_sleep_time': 3600,
                    'ship_style': "1",
                }
            )

        # HELPER METHODS USED BY MAIN ACTIONS. FOR NOW LET'S SKIP OVER _SLEEP AND THE SHIP() METHODS
        def _sleep(self, sleep_length, interval=5):
            self.info("Sleeping %d seconds..." % sleep_length)
            counter = 0
            while counter + interval <= sleep_length:
                sys.stdout.write(".")
                try:
                    time.sleep(interval)
                except:
                    print
                    self.error("Impatient, are we?")
                    sys.exit(1)
                counter += interval
            print
            self.info("Ok, done.")

        def _ship1(self):
            self.info("""
         _~
      _~ )_)_~
      )_))_))_)
      _!__!__!_
      \______t/
    ~~~~~~~~~~~~~
    """)

         # ... ship2() impl
         # ... ship3() impl

        # AH, NAP() OUR FIRST DEFINED ACTION! But where's clobber() you might ask? Remember actions
        # only need to be part of self. We have base impl of clobber() in BaseScript. If that impl
        # suits your needs, no need to overwrite in this class :)
        def nap(self):
            for var_name in self.config.keys():
                if var_name.startswith("random_config_key"):
                    # LOOK, OUR FIRST USE OF SELF.LOG_OBJ. REMEMBER, THIS IS A CONVENIENCE METHOD
                    # self.info(msg)
                    self.info("This is going to be %s!" % self.config[var_name])
            # HERE WE ARE POLLING SELF.CONFIG. REMEMBER IT IS READ ONLY AND AVAILABLE AFTER
            # BaseScript.__init__()
            sleep_time = self.config['long_sleep_time']
            if sleep_time > 60:
                self.info("Ok, grab a %s. This is going to take a while." % self.config['beverage'])
            else:
                self.info("This will be quick, but grab a %s anyway." % self.config['beverage'])
            self._sleep(self.config['long_sleep_time'])

        # NAP TIME IS OVER, TIME TO SHIP IT! OUR FINAL ACTION.
        def ship_it(self):
            name = "_ship%s" % self.config['ship_style']
            if hasattr(self, name):
                # WE USE SELF.CONFIG['SHIP_STYLE'] TO CALL THE APPROPRIATE HELPER METHOD.
                # take a moment to figure out what this will be if you do not pass --ship-style
                # or pass a separate config file with 'ship_style' in it
                getattr(self, name)()


    # __main__ {{{1
    if __name__ == '__main__':
        actions_config_example = ActionsConfigExample()
        # AHA, THIS IS THAT METHOD I MENTIOND AND ANOTHER COMMON IDIOM ON HOW WE KICK OFF OUR SCRIPTS
        actions_config_example.run_and_exit()


Once you've had a read through, play with this script. It's harmless. :)

Try the following calls and see if you can determine why you got the results you did::

     # what actions ran with these calls? How did the behaviour of the actions change? Notice how
     # the script code itself has very minimal conditions and never changes. The config decides all

     # the default nap time is an hour, you might want to ctrl-c this one after a few seconds :)
     python examples/action_config_script.py

     python examples/action_config_script.py --long-sleep-time 5

     python examples/action_config_script.py --long-sleep-time 3  --ship-style 2

     python examples/action_config_script.py --ship-it --ship-style 2

     # this one requires you to make a dummy config file. create a py file that just has the
     # following contents: config = {'ship_style': 3, 'default_actions': ['ship-it']}
     python examples/action_config_script.py --cfg path/to/your/dummy_config.py

Congratulations! If you have followed along, you pretty much understand the core required to read
any mozharness script.

Where do you go from here you might ask?

Here's some things you can do:

    1. BaseMixin provides a number of great helper methods and default actions. Poke through them e.g. run_command is your subprocess friend; it may be long but it should be able to handle all  of your external commands you need to run

    2. outside of BaseMixin, there is a ton of other mixins and base classes you can use for extending the actions at your disposal. Peek in mozharness/base/* and mozharness/mozilla/* . You'll likely find methods for achieving your requirements so you don't even need to impl any new actions. e.g. create_virtualenv(), clone(), setup_mock(), download_file(), make_gaia()

    3. check out the actual scripts/* . Mozharness is used for ~90% of all our jobs done in treeherder. Want to correlate a script to one of those jobs? Open up a log, and grep the mozharness call, likely 'scripts/' or look for the starting log output (timestamp and log level at the start of each line)

    4. take a look at the mozharness FAQ https://developer.mozilla.org/en-US/docs/Mozharness_FAQ

    5. read some blog posts http://escapewindow.dreamwidth.org/tag/mozharness

    6. ready to contribute or work on this project? Check out https://wiki.mozilla.org/Auto-tools/Projects/Mozharness

There is a lot more we can discuss, e.g. using pre and post listeners for setting up or
tearing down actions, decorating pre_config_lock() to manipulate self.config before it locks for the
whole script run, and passing more than one config file to a single script run. However I think
that goes beyond the requirements for navigating or contributing to the Mozharness code base.

.. _Treeherder:

Treeherder
----------
https://wiki.mozilla.org/Auto-tools/Projects/Treeherder

https://treeherder.mozilla.org/

https://treeherder.readthedocs.io/

https://github.com/mozilla/treeherder

?showall=1
?jobname=foo

.. _buildapi:

VCS Sync tools
--------------


.. index:: single: vcs2vcs; legacy

legacy
~~~~~~

The legacy (first implementation) code is in:
    http://hg.mozilla.org/users/hwine_mozilla.com/repo-sync-tools/

The legacy configurations are in:
    http://hg.mozilla.org/users/hwine_mozilla.com/repo-sync-configs/

Documentation is in the code repository, a rendered version of the
latest is at https://people.mozilla.org/~hwine/tmp/vcs2vcs/index.html
