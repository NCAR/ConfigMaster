#!/usr/bin/env python

import os
import sys
import types
import importlib

import argparse

'''
Version 1.3


ChangeLog

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
  ''' This is the main dictionary that holds all the args '''
  opt = {}

  defaultParamsHeader = "#!/usr/bin/env python\n"
  defaultParams = ""
  #optionsToIgnore = ['dt', 'os']
  parser = None
  

  configFilePath = None

  def setDefaultParams(self, dp):
    if dp.lstrip()[0:2] == "#!":
      self.defaultParams = dp
    else:
      self.defaultParams = self.defaultParamsHeader + dp

  def printParams(self):
    print(f"{self.getParamsString()}")
    
  def getParamsString(self):
    returnString=""
    for o in self.opt:
      returnString += (o + " : " + str(self.opt[o]) + "\n")
    return returnString
        
  def assignParameters(self,p):
    global opt
    self.opt = p

  def printDefaultParams(self):
    print(self.defaultParams)

  def assignDefaultParams(self):
#    global defaultParams
#    self.defaultParams = dp
    exec(self.defaultParams, self.opt)
    del self.opt['__builtins__']
    for ko in list(self.opt.keys()):
      if type(self.opt[ko]) == types.ModuleType:
        del self.opt[ko]    

  
  def getConfigFilePath(self):
    return self.configFilePath
        
  # config file path
  def handleConfigFile(self,cfp):
    self.configFilePath = cfp
    config_path, config_file = os.path.split(cfp)

    if config_file[-3:] == ".py":
      config_file = config_file[:-3]

    if config_path != '':
      sys.path.append(config_path)

    #print "importing config file: {}".format(config_file)
    #cf = __import__(config_file, globals(), locals(), [])
    cf = importlib.import_module(config_file)
    for o in self.opt:
      #print "looking at {}".format(o)
      if o in dir(cf):
        #print "found in cf: setting to {}".format(getattr(cf,o))
        self.opt[o] = getattr(cf,o)

    dcf = dir(cf)
    for cfo in dcf:
      #cfo = dcf[kcfo]
      #print cfo,type(cf.__dict__[cfo])      
      if cfo.startswith("__"):# 
        continue
      if type(cf.__dict__[cfo]) == types.ModuleType:
        continue
      if cfo not in self.opt:
        print("\nERROR: Invalid parameter in configuration file {}: {}\n".format(cfp,cfo))
        exit(1)
    

  def init(self, program_description=None, add_param_args=True, add_default_logging=True, additional_args=[]):
    '''
    Parse command line arguments, and initialize parameter dictionary.

    :param str program_description: Short description of the program function. __doc__ is a recommended value.
    :param bool add_param_args: Automatically add command line arguments for configuration parameters
    :param dict additional_args: A collection of dictionaries.  Look at createLogArguments() for an example of its structure.
    '''
    self.assignDefaultParams()

    self.parser = argparse.ArgumentParser(description=program_description, formatter_class=argparse.RawDescriptionHelpFormatter)

    # add possible arguments to the parser
    self.addParseArgs(add_param_args=add_param_args, add_default_logging=add_default_logging,
                        additional_args=additional_args)

    # parse the cmd line and add to opt dictionary
    self.handleArgParse()

    #print(self.opt)
    if add_default_logging:
      self.createDefaultLogger()

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
        logging.basicConfig(format="[[[%(levelname)-9s] [%(asctime)s] -- %(message)s",  level=numeric_level,
                                datefmt='%Y%m%d %H:%M:%S', filename=self.opt["logPath"])
                                                                                  
    
  def createLogArguments(self):

    arglist = []

    posargs = ["-d", "--debugLevel"]
    namedargs = {
      "choices": ["VERBOSE","DEBUG","INFO","WARNING","ERROR","CRITICAL"],
      "help": "Control volume of log messages. (default: %(default)s)",
      "default": "INFO",
      "type": str.upper
      }
    arglist.append( (posargs, namedargs) )

    posargs = ['-l','--logPath']
    namedargs = {
      "help":"The full path to the log file.  Use '-' to log to stdout.  (default: %(default)s)",
      "default":"-"
      }
    arglist.append( (posargs, namedargs) )

    return arglist

  def addAdditionalArguments(self, arglist):
    '''
    Add arguments from arglist to the parser.
    see createLogArguments() for an example of the structure of arglist
    '''  
    for (posargs, namedargs) in arglist:
      self.parser.add_argument(*posargs, **namedargs)

  def handleArgParse(self):
    args = self.parser.parse_args()

    '''
    for o in self.opt:
      #if o in self.optionsToIgnore:
      #  continue
      if o in dir(args):
        if getattr(args,o) != None:
          #print "seting {} to {} from command line".format(o,getattr(args,o))
          self.opt[o] = getattr(args,o)
    '''
    #print(f"{ vars(args).keys()}")
    #print(f"{ self.opt}")
    for o in vars(args).keys():
      if getattr(args,o) != None:
        #print(f"seting {o} to {getattr(args,o)} from command line")
        self.opt[o] = getattr(args,o)
    

  def addParseArgs(self, add_param_args=True, add_default_logging=True, additional_args=[]):
    #parser.add_argument('-c','--config', help="The configuration file.")
    self.parser.add_argument('-c', '--config', help="The configuration file.", action=make_ConfigAction(self))
    self.parser.add_argument('-p', '--print_params', action=make_PrintParamsAction(self.defaultParams),
                        nargs=0, help="Generate a default configuration file.")

    argslist = []
    if add_default_logging:
      argslist = self.createLogArguments()

    argslist += additional_args
    
    self.addAdditionalArguments(argslist)

    if add_param_args:
      self.addAdvancedParseArgs()


    
  def addAdvancedParseArgs(self):
    #self.addParseArgs()

    for o in self.opt:
      #print "o is {} {} {}".format(o,self.opt[o],type(self.opt[o]))
      #if o in self.optionsToIgnore:
      #  continue

      #print "Type of {} is {}".format(o,type(self.opt[o]))
      
      if isinstance(self.opt[o], bool):
        bool_parser = self.parser.add_mutually_exclusive_group(required=False)
        #print "{} is a bool".format(o)
        argument = "--" + o
        action = "store_true"
        helpString = "Set " + o + " to True"
        bool_parser.add_argument(argument, action=action, help=helpString, default=None)
        argument = "--no-" + o
        action = "store_false"
        helpString = "Set " + o + " to False"
        bool_parser.add_argument(argument, action=action, help=helpString, default=None)
      elif isinstance(self.opt[o], (int,float,str)):
        #print "working on {}".format(o)
        argument = "--" + o
        helpString = "Overide the param file value of " + o
        self.parser.add_argument(argument, help=helpString)
              
      
  def __getitem__(self, key):
      return self.opt[key]

  def __setitem__(self, key, value):
      global opt
      self.opt[key] = value
			
			
			
		

