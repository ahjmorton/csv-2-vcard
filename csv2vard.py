#!/usr/bin/python

import sys
import os
import csv
import re

_CARD_HEADER = "BEGIN:VCARD"
_CARD_VERSION = "VERSION:2.1"
_CARD_LINE_BREAK = "".join((chr(13),chr(10))) 
_CARD_FOOTER = "END:VCARD"

_HOME_PHONE = "General phone"
_FIRST_NAME = "First name"
_SUR_NAME = "Last name"
_CELL_PHONE = "General mobile"
_EMAIL_ADDR = "General email"

class FieldHandler(object) :
    def __init__(self, test_function, format_func) :
        self.format_func = format_func
        self.test = test_function

    def can_handle(self, field_mapping) :
        return self.test(field_mapping)

    def handle(self, field_mapping) :
        return self.format_func(field_mapping)

class ChainTest(object) :
    def __init__(self, func) :
        self.chain = [func]

    def __call__(self, value) :
        for func in self.chain :
            if not func(value) :
               return False
        return True
  
    def that(self, func) :
        self.chain.append(func)
        return self

def chainable(func) :
    return ChainTest(func)

def haveAll(*required) :
    def required_func_driver(field_mapping) :
        for req in required :
            if req not in field_mapping:
                return False
        return True
    return chainable(required_func_driver)

def have(required) :
    return haveAll(required)

def have_any(*fields) :
    def have_any_driver(field_mappings) :
        for field in field_mappings :
            if field in fields :
               return True
        return False
    return chainable(have_any_driver)

def is_phone(field_name, *other_types) :
    def phone_driver(field_mappings) :
        phone_no = field_mappings[field_name]
        types = "VOICE"
        other_len = len(other_types)
        if other_len == 1 :
            types += ";" + other_types[0]
        elif other_len > 1 :
            types += ";" + ";".join(other_types)
        return "TEL;{}:{}".format(types, phone_no)
    return phone_driver

def is_home_phone(field) :
    return is_phone(field, "HOME")

def is_mobile_phone(field) :
    return is_phone(field, "CELL")

def is_name() :
    def is_name_driver(fields) :
        first_name = "" if _FIRST_NAME not in fields else fields[_FIRST_NAME]
        sur_name = "" if _SUR_NAME not in fields else fields[_SUR_NAME]
        return "N:{};{};;;".format(sur_name, first_name)
    return is_name_driver

def is_formatted_name() :
    def is_name_driver(fields) :
        first_name = "" if _FIRST_NAME not in fields else fields[_FIRST_NAME]
        sur_name = "" if _SUR_NAME not in fields else fields[_SUR_NAME]
        formatted = "{} {}".format(first_name, sur_name).strip()
        return "FN:{}".format(formatted) 
    return is_name_driver

def is_email() :
    def is_email_driver(fields) :
        return "EMAIL;INTERNET:{}".format(fields[_EMAIL_ADDR])
    return is_email_driver

def looks_like(field_name, test) :
    def looks_like_driver(fields) :
        return test(fields[field_name])
    return looks_like_driver

_is_home = lambda x : x.startswith("020")

_MOBILE_REGEX = re.compile("(\+?44|0)7[4-9]")

def _is_mobile(number) :
    return _MOBILE_REGEX.match(number) is not None

def _is_other(number) :
    return not _is_home(number) and not _is_mobile(number)

def looks_like_home(field_name) :
    return looks_like(field_name, _is_home)

def looks_like_mobile(field_name) :
    return looks_like(field_name, _is_mobile)

def looks_like_other(field_name) : 
    return looks_like(field_name, _is_other)


def fields(test, format) :
    return FieldHandler(test, format)

_FIELD_HANDLERS = ([
    fields(have_any(_FIRST_NAME, _SUR_NAME), is_name()),
    fields(have_any(_FIRST_NAME, _SUR_NAME), is_formatted_name()),

    fields(have(_HOME_PHONE).that(looks_like_home(_HOME_PHONE)), is_home_phone(_HOME_PHONE)),
    fields(have(_HOME_PHONE).that(looks_like_mobile(_HOME_PHONE)), is_mobile_phone(_HOME_PHONE)),
    fields(have(_HOME_PHONE).that(looks_like_other(_HOME_PHONE)), is_phone(_HOME_PHONE)),

    fields(have(_CELL_PHONE), is_mobile_phone(_CELL_PHONE)),

    fields(have(_EMAIL_ADDR), is_email())
])

def filter_empty(adict) :
    new_dict = dict()
    for key in adict :
        if adict[key] :
            new_dict[key] = adict[key]
    return new_dict

def _is_valid(lines) :
    return (
len(lines) >= 4 and 
lines[0] == _CARD_HEADER and
lines[1] == _CARD_VERSION and
any(map(lambda x : x.startswith("N:"), lines)) and
lines[len(lines) - 1] == _CARD_FOOTER
)

def build_vcard(field_mapping) :
    card_lines = []
    card_lines.append(_CARD_HEADER)
    card_lines.append(_CARD_VERSION)
    for handler in _FIELD_HANDLERS :
        if handler.can_handle(field_mapping) :
            card_lines.append(handler.handle(field_mapping))
    card_lines.append(_CARD_FOOTER)
    if _is_valid(card_lines) :
        return _CARD_LINE_BREAK.join(card_lines) + _CARD_LINE_BREAK
    else :
        return ""

def main(file_loc, output=None) :
    output = file_loc + ".vcf" if output is None else output
    with open(file_loc, "r") as infile :
        with open(output, "a") as outfile :
            for row in csv.DictReader(infile) :
                outfile.write(build_vcard(filter_empty(row)))

if __name__ == '__main__' :
    if len(sys.argv) < 2 :
        sys.exit("Usage: {0} <contacts_csv>".format(sys.argv[0]))
    if not os.path.exists(sys.argv[1]) :
        sys.exit("ERROR: cannot find input file") 
    main(sys.argv[1])
