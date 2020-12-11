#!/usr/bin/env python

import os
import sys
import types
import importlib.util

import argparse

'''
Version 1.6


ChangeLog
1.6 - Added handling for __file__
1.5 - Added _config_override support
1.4 - Fixed type being set incorrectly when using cmd line options, added simple init. 
1.3 - Added index operator support
1.2 - Added automatic logging support
'''


# Create an Action subclass that prints the
# default params for us without having to force the user to query the argparse
# print_params by hand
def make_PrintParamsAction(paramString):
    class CMPPAction(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            print(paramString)
            setattr(args, self.dest, values)
            exit(1)

    return CMPPAction


def make_ConfigAction(cm):
    class CMCAction(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            cm.handleConfigFile(values)

    return CMCAction


class ConfigMaster:
    """ This is the main dictionary that holds all the args """
    opt = {}

    defaultParamsHeader = "#!/usr/bin/env python3\n"
    defaultParams = ""
    # optionsToIgnore = ['dt', 'os']
    parser = None

    # this hangs on to a reference of the cmd line args for us.
    args = None

    version_info = (1, 6)
    version = ".".join(map(str, version_info))

    configFilePath = None
    allow_extra_parameters = False

    allow_config_override = True
    config_override_dict_name = "_config_override"

    doDebug = False

    # dumb default constructor does nothing.
    # TODO - should the assignments above be in a constructor?

    # Instead of this:
    # p = ConfigMaster()
    # p.setDefaultParams(defaultParams)
    # p.init(__doc__, add_default_logging=True, allow_extra_parameters=True)

    # waant to just do this
    # p = ConfigMaster(defaultParams, __doc__, add_default_logging=True, allow_extra_parameters=True)
    # parameterized constructor
    def __init__(self, defaultParams=None, docString="", **kwargs):

        # print(kwargs)
        # to be backwards compatible, we support the old method of setting up ConfigMaster with 3 different calls
        if defaultParams != None:
            self.setDefaultParams(defaultParams)
        
        self.init(docString, **kwargs)


    def debug(self, s):
        #print(f"dd = {self.doDebug}")
        if self.doDebug:
            print(s)

    def setDefaultParams(self, dp):
        if dp.lstrip()[0:2] == "#!":
            self.defaultParams = dp
        else:
            self.defaultParams = self.defaultParamsHeader + dp

    def printParams(self):
        print(f"{self.getParamsString()}")

    def getParamsString(self):
        returnString = ""
        for o in self.opt:
            if self.allow_config_override and not self.config_override_dict_name == o:
                returnString += (o + " : " + str(self.opt[o]) + "\n")
        return returnString

    def assignParameters(self, p):
        global opt
        self.opt = p

    def printDefaultParams(self):
        print(self.defaultParams)

    def assignDefaultParams(self):
        #    global defaultParams
        #    self.defaultParams = dp
        #  self.opt["_config_override"] = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(list)))
        dp = self.defaultParams
        if self.allow_config_override:
            dp = f"import collections\n{self.config_override_dict_name} = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(list)))\n" + dp
        exec(dp, self.opt)
        #print("opt ")
        #print(self.opt)
        del self.opt['__builtins__']

        # make a copy of the keys because we are going to be deleting as we iterate
        ko_keys = list(self.opt.keys())
        for ko in ko_keys:
            if type(self.opt[ko]) == types.ModuleType:
                del self.opt[ko]

    def getConfigFilePath(self):
        return self.configFilePath

    # config file path
    def handleConfigFile(self, cfp):
        self.configFilePath = cfp
        config_path, config_file = os.path.split(cfp)

        if config_file[-3:] == ".py":
            config_file = config_file[:-3]

        if config_path != '':
            sys.path.append(config_path)

        # print "importing config file: {}".format(config_file)
        # cf = __import__(config_file, globals(), locals(), [])

        # cf = importlib.import_module(config_file)

        print(f"loading configuration from {cfp}")
        with open(cfp, 'r') as my_conf_file:
            conf_string = my_conf_file.read()
        #print(f"conf_str = {conf_string}")
        #spec = importlib.util.spec_from_file_location(config_file, cfp)
        #cf = importlib.util.module_from_spec(spec)
        #spec.loader.exec_module(cf)
        cf = {}
        if self.allow_config_override:
            conf_string = f"import collections\n{self.config_override_dict_name} = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(list)))\n" + conf_string

        # when I switched from importlib back to exec, __file__ stopped working, so swap by hand:
        conf_string = conf_string.replace("__file__","'"+config_file+"'")

        #self.debug(f"about to exec:\n {conf_string}\n\n")
        try:
            exec(conf_string, cf)
        except: 
            print(f"FAIL: exec of conf_string:\n{conf_string}\n")
            raise
        
        del cf['__builtins__']
        #for cfk in list(cf.keys()):
        #    if type(cf[cfk]) == types.ModuleType:
        #        del cf[cfk]

        # cf = importlib.import_module(config_file)
        for o in self.opt:
            #self.debug(f"looking at {o}")
            #if o == self.config_override_dict_name:
            #    continue
            #if o in dir(cf):
            #    self.debug(f"found in cf: setting to {getattr(cf, o)}")
            #    self.opt[o] = getattr(cf, o)
            if o in cf:
                self.debug(f"found {o} in config file\n\toverriding to {cf[o]}")
                self.opt[o] = cf[o]

        #dcf = dir(cf)
        #self.debug(f"cf = {cf}")
        #self.debug(f"dcf = {dcf}")

        # make a copy of the keys because we are going to be deleting them.
        #cf_keys = list(cf.keys())

        #print (cf)
        for cfo in cf:
            #self.debug(f"cfo = {cfo}  type={type(cfo)}")
            # cfo = dcf[kcfo]
            # print cfo,type(cf.__dict__[cfo])
            if cfo.startswith("__"):  #
                continue
            #if type(cf.__dict__[cfo]) == types.ModuleType:
            #    continue
            if type(cf[cfo]) == types.ModuleType:
                continue
            #print(f"{cfo} = {type(cfo)}")
            #print(f"{cf[cfo]} = {type(cf[cfo])}")
            if cfo not in self.opt:
                if self.allow_extra_parameters:
                    print("WARNING: Extra parameter in configuration file {}: {}\n".format(cfp, cfo))
                    self.opt[cfo] = cf[cfo]
                else:
                    print("\nERROR: Invalid parameter in configuration file {}: {}\n".format(cfp, cfo))
                    exit(1)

    def init(self, program_description=None, add_param_args=True, add_default_logging=True, additional_args=None,
             allow_extra_parameters=None, doDebug=False):
        """
        Parse command line arguments, and initialize parameter dictionary.

        :param doDebug: Turn on ConfigMaster debugging
        :param add_default_logging: This can be used to turn on/off the --debugString and --logPath options
        :param allow_extra_parameters: If this is true, then ConfigMaster will merely warn and not exit if an extra parameter is found in the config file.
        :param str program_description: Short description of the program function. __doc__ is a recommended value.
        :param bool add_param_args: Automatically add command line arguments for configuration parameters
        :param dict additional_args: A collection of dictionaries.  Look at createLogArguments() for an example of its structure.
        """
        #print(f"dd = {doDebug}")
        self.doDebug = doDebug
        #print(f"dd = {self.doDebug}")

        if allow_extra_parameters is not None:
            self.allow_extra_parameters = allow_extra_parameters

        #print("initial params")
        #self.printParams()
        self.assignDefaultParams()

        #print("after default assigned")
        #self.printParams()
        self.parser = argparse.ArgumentParser(description=program_description,
                                              formatter_class=argparse.RawDescriptionHelpFormatter)

        # add possible arguments to the parser
        self.addParseArgs(add_param_args=add_param_args, add_default_logging=add_default_logging,
                          additional_args=additional_args)

        # parse the cmd line and add to opt dictionary
        self.handleArgParse()
        #print("after arg parse")
        #self.printParams()

        # print(f" aco = {self.allow_config_override}")
        if self.allow_config_override:
            self.doConfigOverride()
            self.handleArgParse()

        #print("after config override")
        #self.printParams()


        # print(self.opt)
        if add_default_logging:
            self.createDefaultLogger()

    def doConfigOverride(self):
        #print("t")
        # _config_override["model"]["GFS5"]["min_expected_filesize"] = 160e+6  # 160M

        # self.debug("doConfigOverride")
        for param1 in self.opt[self.config_override_dict_name]:
            self.debug(f"Using {param1} for overriding")
            for param1_target in self.opt[self.config_override_dict_name][param1]:
                self.debug(f"If user sets {param1} to {param1_target} on the cmd line")
                for param2 in self.opt[self.config_override_dict_name][param1][param1_target]:
                    param2_target = self.opt[self.config_override_dict_name][param1][param1_target][param2]
                    self.debug(f"If user sets {param1} to {param1_target} (on the cmd line), then {param2} gets set to {param2_target}")
                    if getattr(self.args, param1) == param1_target:
                        self.opt[param2] = param2_target
                        self.debug(f"overriding {param2} with {param2_target} ({self.config_override_dict_name})")

    def createDefaultLogger(self):

        import logging
        # Add custom verbose logging level
        logging.VERBOSE = 5
        logging.addLevelName(logging.VERBOSE, "VERBOSE")
        logging.Logger.verbose = lambda inst, msg, *args, **kwargs: inst.log(logging.VERBOSE, msg, *args, **kwargs)
        logging.verbose = lambda msg, *args, **kwargs: logging.log(logging.VERBOSE, msg, *args, **kwargs)

        numeric_level = getattr(logging, self.opt["debugLevel"].upper(), None)

        # in theory should never get here, because argparse should restrict us to valid levels
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % self.opt["debugLevel"])

        if self.opt["logPath"] == "-":
            print("Logging to stdout")
            logging.basicConfig(format="[%(levelname)-8s] [%(asctime)s] -- %(message)s",
                                level=numeric_level, datefmt='%Y%d%m %H:%M:%S', stream=sys.stdout)
        else:
            print(f"Logging to {self.opt['logPath']}")
            logging.basicConfig(format="[[[%(levelname)-9s] [%(asctime)s] -- %(message)s", level=numeric_level,
                                datefmt='%Y%m%d %H:%M:%S', filename=self.opt["logPath"])

    def createLogArguments(self):

        arglist = []

        posargs = ["-d", "--debugLevel"]
        namedargs = {
            "choices": ["VERBOSE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            "help": "Control volume of log messages. (default: %(default)s)",
            "default": "INFO",
            "type": str.upper
        }
        arglist.append((posargs, namedargs))

        posargs = ['-l', '--logPath']
        namedargs = {
            "help": "The full path to the log file.  Use '-' to log to stdout.  (default: %(default)s)",
            "default": "-"
        }
        arglist.append((posargs, namedargs))

        return arglist

    def addAdditionalArguments(self, arglist):
        '''
        Add arguments from arglist to the parser.
        see createLogArguments() for an example of the structure of arglist
        '''
        for (posargs, namedargs) in arglist:
            self.parser.add_argument(*posargs, **namedargs)

    def handleArgParse(self):
        """
        This can be called multiple times to have the cmd line args ovveride other values, but it will only
        actually parse the args (and therefore the config file) the first time it is called.
        :return:
        """
        if self.args == None:
            self.args = self.parser.parse_args()


        '''
        for o in self.opt:
          #if o in self.optionsToIgnore:
          #  continue
          if o in dir(args):
            if getattr(args,o) != None:
              #print "seting {} to {} from command line".format(o,getattr(args,o))
              self.opt[o] = getattr(args,o)
        '''
        # print(f"{ vars(args).keys()}")
        # print(f"{ self.opt}")
        for o in vars(self.args).keys():
            if getattr(self.args, o) != None:
                # print(f"seting {o} to {getattr(self.args,o)} from command line")
                self.opt[o] = getattr(self.args, o)

    def addParseArgs(self, add_param_args=True, add_default_logging=True, additional_args=None):
        # parser.add_argument('-c','--config', help="The configuration file.")
        self.parser.add_argument('-c', '--config', help="The configuration file.", action=make_ConfigAction(self))
        self.parser.add_argument('-p', '--print_params', action=make_PrintParamsAction(self.defaultParams),
                                 nargs=0, help="Generate a default configuration file.")

        argslist = []
        if add_default_logging:
            argslist = self.createLogArguments()

        if additional_args is not None:
            argslist += additional_args

        self.addAdditionalArguments(argslist)

        if add_param_args:
            self.addAdvancedParseArgs()

    def addAdvancedParseArgs(self):
        # self.addParseArgs()

        for o in self.opt:
            # print "o is {} {} {}".format(o,self.opt[o],type(self.opt[o]))
            # if o in self.optionsToIgnore:
            #  continue

            # print "Type of {} is {}".format(o,type(self.opt[o]))

            if isinstance(self.opt[o], bool):
                bool_parser = self.parser.add_mutually_exclusive_group(required=False)
                # print "{} is a bool".format(o)
                argument = "--" + o
                action = "store_true"
                helpString = "Set " + o + " to True"
                bool_parser.add_argument(argument, action=action, help=helpString, default=None)
                argument = "--no-" + o
                action = "store_false"
                helpString = "Set " + o + " to False"
                bool_parser.add_argument(argument, action=action, help=helpString, default=None, dest=o)
            elif isinstance(self.opt[o], (int, float, str)):
                # print "working on {}".format(o)
                argument = "--" + o
                helpString = "Overide the param file value of " + o
                self.parser.add_argument(argument, help=helpString, type=type(self.opt[o]))

    def __getitem__(self, key):
        return self.opt[key]

    def __setitem__(self, key, value):
        global opt
        self.opt[key] = value
