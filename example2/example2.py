#!/usr/bin/env python

# This program uses an external file for the default params

import example2_pdef as P

def main():
    p = P.Params()
    p.init("A simple Example Program",add_default_logging=False)
    
    print("Using these parameters")
    p.printParams()


if __name__ == "__main__":
    main()

