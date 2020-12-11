# ConfigMaster
A light-weight tool for python which handles configuration, command line options, and logging in a easy to use package (requires only one line of code).

Here is an example of the simplest usage:
```python
#!/usr/bin/env python3
'''
Super simple example of ConfigMaster
'''

from ConfigMaster import ConfigMaster
import logging

defaultParams = """
import os, datetime

forecastHour = 4
dataDir = "/dir"
outFile = os.path.join(dataDir,"output",datetime.datetime.now().strftime("%Y%m%d") + ".out")
"""

p = ConfigMaster(defaultParams, __doc__, add_default_logging=True)

logging.info(f"forecastHour = {p['forecastHour']}")
```

```bash
$ ./simple.py -h
usage: simple.py [-h] [-c CONFIG] [-p]
                 [-d {VERBOSE,DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-l LOGPATH]
                 [--forecastHour FORECASTHOUR] [--dataDir DATADIR]
                 [--outFile OUTFILE]

Super simple example of ConfigMaster

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        The configuration file.
  -p, --print_params    Generate a default configuration file.
  -d {VERBOSE,DEBUG,INFO,WARNING,ERROR,CRITICAL}, --debugLevel {VERBOSE,DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Control volume of log messages. (default: INFO)
  -l LOGPATH, --logPath LOGPATH
                        The full path to the log file. Use '-' to log to
                        stdout. (default: -)
  --forecastHour FORECASTHOUR
                        Overide the param file value of forecastHour
  --dataDir DATADIR     Overide the param file value of dataDir
  --outFile OUTFILE     Overide the param file value of outFile


$ ./simple.py 
Logging to stdout
[INFO    ] [20201112 13:27:46] -- forecastHour = 4
```

ConfigMaster provides reading and automatic generation of parameter files, default parameter values, automatic command line overrides, consistent logging to a file or stdout, (including debug level control from the command line) and more:

* Ability to easily generate a default parameter file (i.e --print_params capability).  The documentation included in the file helps the new user to understand the use of the program and customize the parameters.
* Automatic support for logging (log file or stdout), and debug levels.
* Simple default behavior. If no parameter file is used (or some parameters are missing), the default parameter values are used.
* Warning if you give a parameter in your config file that it doesn't expect (can be turned off).
* Automatically generate command line overrides for configuration parameters.
  * Only for int, long, float, string, and bool types currently
* Automatic generation of usage statements.
* Self-documenting. All parameter documentation is done in the paramdef, therefore the documentation and code are co-located, making it easy to keep the documentation up-to-date.
* Support for environment variables in the parameter files.
  * Other python code can also be included in the param files - date/time logic, file system logic, etc.
* Separation of parameter definition from script logic (i.e. tdrp's paramdef file).
  * A separate paramdef file is optional (constrast examples 1 & 2 below)).
* Encapsulation of parameter handling logic  (contained in the ConfigMaster class)
* Simple.  Requires one line of code (not counting the import).


# Installation

1. Check out ConfigMaster.py from cvs and put it in a location that is in your $PYTHONPATH.
1. That's it.

# Repository Location

* ConfigMaster for Python2.x is in cvs at libs/python/src/ConfigMaster
* ConfigMaster for Python3 is in github at https://github.com/NCAR/ConfigMaster

# Examples

When you clone the repository, you will also get several subdirectories named example1 to example{N}.  

Examples 4 is the  most useful examples. I recommend you start there.  Here is a short description of the other examples.

* **Example 1** - A simple example with logging support turned off.
* **Example 2** - Similar to example 1, but shows you how to put your parameter definitions in a separate file, instead of within the script itself.  Logging support is off.
* **Example 3** - Same as example 1, except it also uses environment variables, and logic in the param file.  Logging support is off.

### Example 4
* Defines the configuration file in the script
* Integrated logging enabled.

[Example4.py Source](https://raw.githubusercontent.com/NCAR/ConfigMaster/master/example4/example4.py)

#### Output
Here is what the usage statement looks like:
```
$ ./example4.py -h
usage: example4.py [-h] [-c CONFIG] [-p]
                   [-d {VERBOSE,DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                   [-l LOGPATH] [--forecastHour FORECASTHOUR]
                   [--emailAddress EMAILADDRESS] [--dataDir DATADIR]
                   [--outFile OUTFILE]

A simple script to show how ConfigMaster works with Logging integration.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        The configuration file.
  -p, --print_params    Generate a default configuration file.
  -d {VERBOSE,DEBUG,INFO,WARNING,ERROR,CRITICAL}, --debugLevel {VERBOSE,DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Control volume of log messages. (default: INFO)
  -l LOGPATH, --logPath LOGPATH
                        The full path to the log file. Use '-' to log to
                        stdout. (default: -)
  --forecastHour FORECASTHOUR
                        Overide the param file value of forecastHour
  --emailAddress EMAILADDRESS
                        Overide the param file value of emailAddress
  --dataDir DATADIR     Overide the param file value of dataDir
  --outFile OUTFILE     Overide the param file value of outFile$ ./example4/example4.py -h
```

Here is what example4 looks like when run:
```
$ ./example4.py
Logging to stdout
[INFO    ] [20191605 09:26:29] -- Using these parameters:
[INFO    ] [20191605 09:26:29] --       forecastHour : 3
[INFO    ] [20191605 09:26:29] --       emailAddress : prestop@ucar.edu
[INFO    ] [20191605 09:26:29] --       dataDir : /home/prestop/data
[INFO    ] [20191605 09:26:29] --       outFile : /home/prestop/data/output/20190516.out
[INFO    ] [20191605 09:26:29] --       debugLevel : INFO
[INFO    ] [20191605 09:26:29] --       logPath : -
[INFO    ] [20191605 09:26:29] -- info test
[WARNING ] [20191605 09:26:29] -- ./example4.py:25: DeprecationWarning: The 'warn' function is deprecated, use 'warning' instead
  logging.warn("warn test")

[WARNING ] [20191605 09:26:29] -- warn test
You access the configuration using p.opt['key'].  e.g. emailAddress: prestop@ucar.edu
```

# Order of Precedence
1. Command line
1. _config_override  (see [Advanced Documention - Configuration Override](README_advanced.md#configuration-override) )
1. Config File 
1. Default (Config Definition) Arguments

# Additional documentation
In an effort to keep this front page less cluttered advanced features and additional information has been moved to the  [Advanced Documention](README_advanced.md).
 
Documentation on the UCAR wiki goes into more detail for examples one, two, and three.
https://wiki.ucar.edu/display/ral/ConfigMaster.py

