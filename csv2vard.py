#!/usr/bin/python

import sys
import os
import csv


def main(file_loc, output=None) :
    output = file_loc + ".csv" if output is None else output
    with open(file_loc, "r") as infile :
        with open(output, "a") as outfile :
            pass

if __name__ == '__main__' :
    if len(sys.argv) < 2 :
        sys.exit("Usage: {0} <contacts_csv>".format(sys.argv[0]))
    if not os.path.exists(sys.argv[1]) :
        sys.exit("ERROR: cannot find input file") 
    main(argv[0])
