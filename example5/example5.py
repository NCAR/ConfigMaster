#!/usr/bin/env python
"""
A simple script to show how ConfigMaster works with _config_override
Try passing --model GFS4 or --model GFS5 to see how it changes the other parameters.
"""
from ConfigMaster import ConfigMaster

import logging
import os

defaultParams = """
import os
import datetime

#####################################
## GENERAL CONFIGURATION
#####################################

#possible values: GFS3, GFS4 or GFS5
model = "GFS3" 
expected_file_size = 10e+7
forecast_hours = 24

_config_override["model"]["GFS4"]["expected_file_size"] = 15e+7
_config_override["model"]["GFS4"]["forecast_hours"] = 36
_config_override["model"]["GFS5"]["expected_file_size"] = 20e+7
_config_override["model"]["GFS5"]["forecast_hours"] = 48
"""

# It can be convenient to give your ConfigMaster instance global scope
p = ConfigMaster(defaultParams, __doc__, add_default_logging=True, allow_extra_parameters=True)
print(f"Using ConfigMaster version {p.version}")


def main():
    logging.info(f"Using these parameters:")
    for key in p.opt:
        if not key == "_config_override":
            logging.info(f"\t{key} : {p[key]}")

if __name__ == "__main__":
    main()
