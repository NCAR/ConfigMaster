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

