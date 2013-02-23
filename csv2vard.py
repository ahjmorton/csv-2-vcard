#!/usr/bin/python

import sys
import os
import csv

_CARD_HEADER = "BEGIN:VCARD"
_CARD_VERSION = "VERSION:4.0"
_CARD_LINE_BREAK = "".join((chr(13),chr(10))) 
_CARD_FOOTER = "END:VCARD"

def build_vcard(field_mappings) :
    card_lines = []
    card_lines.append(_CARD_HEADER)
    card_lines.append(_CARD_VERSION)
    card_lines.append(_CARD_FOOTER)
    return _CARD_LINE_BREAK.join(card_lines) + _CARD_LINE_BREAK

def main(file_loc, output=None) :
    output = file_loc + ".vcf" if output is None else output
    with open(file_loc, "r") as infile :
        with open(output, "a") as outfile :
            for row in csv.DictReader(infile) :
                outfile.write(build_vcard(row))

if __name__ == '__main__' :
    if len(sys.argv) < 2 :
        sys.exit("Usage: {0} <contacts_csv>".format(sys.argv[0]))
    if not os.path.exists(sys.argv[1]) :
        sys.exit("ERROR: cannot find input file") 
    main(sys.argv[1])
