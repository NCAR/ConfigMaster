#!/usr/bin/env python

import example2_pdef as P

def main():
    p = P.Params()
    p.init("A simple Example Program",add_default_logging=False)
    
    print("Using these parameters")
    p.printParams()


if __name__ == "__main__":
    main()

