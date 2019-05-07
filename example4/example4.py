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
emailAddy = "prestop@ucar.edu"

dataDir = os.path.join(os.environ["HOME"],"data")

logFile = os.path.join(dataDir,"logs",datetime.datetime.now().strftime("%Y%m%d") + ".log")
 
"""


if __name__ == "__main__":
    main()