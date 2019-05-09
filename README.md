# ConfigMaster
A light-weight tool for python configuration which provides automatic generation of parameter files, default parameter values, automatic command line overrides, and more. The design was influenced by TDRP (Table-Driven Runtime Parameters).


ConfigMaster provides:

* Ability to easily generate a default parameter file (i.e --print_params capability).  The documentation included in the file helps the new user to understand the use of the program and customize the parameters.
* Encapsulation of parameter handling logic  (contained in the ConfigMaster class)
* Simple default behavior. If no parameter file is used, the default parameter values are used.
  * Overriding of missing parameters with default values.
* Warning if you give a parameter in your config file that it doesn't expect.
* Automatic command line override for configuration parameters.
  * Only for int, long, float, string, and bool types currently
* Self-documenting. All parameter documentation is done in the paramdef, therefore the documentation and code are co-located, making it easy to keep the documentation up-to-date.
* Support for environment variables in the parameter files.
  * Other python code can also be included in the param files - date/time logic, file system logic, etc.
* Separation of parameter definition from script logic (i.e. tdrp's paramdef file).
  * A separate paramdef file is optional (constrast examples 1 & 2 below)).
* Automatic support for logging (log file or stdout), and debug levels.
* Simple.  Minimal coding required. Most work is done in the the paramdef file.


# Installation

1. Check out ConfigMaster.py from cvs and put it in a location that is in your $PYTHONPATH.
1. That's it.

# Repository Location

* ConfigMaster for Python2.x is in cvs at libs/python/src/ConfigMaster
* ConfigMaster for Python3 is in github at https://github.com/NCAR/ConfigMaster

# Examples

When you clone the repository, you will also get several subdirectories named example1 to example{N}.  

Example 4 is the latest, and most useful example.  Since it is still relatively simple, and will fit most users needs, I recomend you start there.

## Example 1
A simple example with logging support turned off.

## Example 2
Similar to example 1, but shows you how to put your parameter definitions in a separate file, instead of within the script itself.  Logging support is off.

## Example 3
Same as example 1, except it also uses environment variables, and logic in the param file.  Logging support is off.

## Example 4
This example uses configuration defintion in the script and has the integrated logging enabled.
```python
#!/usr/bin/env python
'''
A simple script to show how ConfigMaster works with Logging integration.
'''
from ConfigMaster import ConfigMaster

import logging
logging.captureWarnings(True)


def main():
    p = ConfigMaster()
    p.setDefaultParams(defaultParams)
    p.init(__doc__, add_default_logging=True)

    logging.info(f"Using these parameters:")
    for line in p.getParamsString().splitlines():
        logging.info(f"\t{line}")
    
    logging.info("info test")
    logging.debug("debug test")
    logging.warning("warn test")


defaultParams = """
import os
import datetime
#####################################
## GENERAL CONFIGURATION
#####################################

# Forecast hour
if datetime.datetime.now().hour % 2 == 0:
  forecastHour = 4
else:
  forecastHour = 3

# Email Address
emailAddress = "prestop@ucar.edu"

dataDir = os.path.join(os.environ["HOME"],"data")

outFile = os.path.join(dataDir,"output",datetime.datetime.now().strftime("%Y%m%d") + ".out")
"""


if __name__ == "__main__":
    main()
```

### Output
Here is what the usage statement looks like:
```
$ ./example4/example4.py -h
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
  --outFile OUTFILE     Overide the param file value of outFile
```

Here is what example4 looks like when run:
```
$ ./example4/example4.py
Logging to stdout
[INFO    ] [20190905 14:30:15] -- Using these parameters:
[INFO    ] [20190905 14:30:15] -- 	forecastHour : 4
[INFO    ] [20190905 14:30:15] -- 	emailAddress : prestop@ucar.edu
[INFO    ] [20190905 14:30:15] -- 	dataDir : /home/prestop/data
[INFO    ] [20190905 14:30:15] -- 	outFile : /home/prestop/data/output/20190509.out
[INFO    ] [20190905 14:30:15] -- 	debugLevel : INFO
[INFO    ] [20190905 14:30:15] -- 	logPath : -
[INFO    ] [20190905 14:30:15] -- info test
[WARNING ] [20190905 14:30:15] -- ./example4.py:25: DeprecationWarning: The 'warn' function is deprecated, use 'warning' instead
  logging.warn("warn test")

[WARNING ] [20190905 14:30:15] -- warn test
```

# Additional documentation
Documentation on the UCAR wiki goes into more detail for examples one, two, and three.
https://wiki.ucar.edu/display/ral/ConfigMaster.py
