#!/usr/bin/env python
'''
A simple script to show how ConfigMaster works with Logging integration.
'''
from ConfigMaster import ConfigMaster

import logging

import os

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

test = True
"""


# It can be convenient to give your ConfigMaster instance global scope
p = ConfigMaster(defaultParams, __doc__, add_default_logging=True, allow_extra_parameters=True)
print(f"Using ConfigMaster version {p.version}")

def main():

    logging.info(f"Using these parameters:")
    for line in p.getParamsString().splitlines():
        logging.info(f"\t{line}")
    
    logging.info("info test")
    logging.debug("debug test")

    logging.warning("warning test")

    print(f"\nEXAMPLE - You access the configuration using p['key'].  e.g. emailAddress: {p['emailAddress']}")

    # you can also use your ConfigMaster object to store other derived configuration values
    # I recommend using an '_' prefix to differentiate these added values
    p["_newDir"] = os.path.join(p["dataDir"], "new")
    print(f"\nPassing around this other value: {p['_newDir']}")
    

    

if __name__ == "__main__":
    main()
