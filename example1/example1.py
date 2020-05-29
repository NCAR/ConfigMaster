#!/usr/bin/env python

'''
A simple script to show how ConfigMaster works.
'''
from ConfigMaster import ConfigMaster

defaultParams = """
#####################################
## GENERAL CONFIGURATION
#####################################
 
## debug ##
# Flag to output debugging information
debug = False

# Forecast hour
forecastHour = 3

# Email Address
emailAddy = "prestop@ucar.edu"
 
"""

def main():
    p = ConfigMaster()
    p.setDefaultParams(defaultParams)
    p.init(__doc__, add_default_logging=False)

    print(f"Using ConfigMaster version {p.version}")
    
    print("Using these parameters")
    p.printParams()

    if p["debug"]:
        print(f"\nDEBUG: Using forecast hour: {p['forecastHour']}")





if __name__ == "__main__":
    main()
