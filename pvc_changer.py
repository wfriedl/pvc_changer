#!/usr/bin/env python2.7

"""
    A tool to update the Product Version and Code of a C# VS2010 setup package (*.vdproj).  Intended
    to be used with an automated build process.

"""

import re
import uuid
import argparse 
import os, shutil
import tempfile

##"ProductCode" = "8:{35424778-8534-431B-9492-5CD84B1EDE03}"
productcode_re = re.compile(r"(?:\"ProductCode\" = \"8.){([\d\w-]+)}")

##"ProductVersion" = "8:1.0.89"
productversion_re = re.compile(r"(?:\"ProductVersion\" = \"8.)([\d\w\.]+)\"")


def replace_code_and_version(src_fname, version="1.0.0", code="12345678-1234-1234-1234-1233456789012"):
    fd, tmp_fname = tempfile.mkstemp()
    tmp = open(tmp_fname, 'w')
    src = open(src_fname)
    for l in src:
        if productcode_re.search(l):
            m = productcode_re.search(l)
            l = l.replace(m.group(1), code)
        if productversion_re.search(l):
            m = productversion_re.search(l)
            l = l.replace(m.group(1), version)
        tmp.write(l)
    tmp.close()
    os.close(fd)
    src.close()
    os.remove(src_fname)
    shutil.move(tmp_fname, src_fname)


def parse_commands(test_args=None):
    descrip = "Utility to update ProductCode and ProductVersion of VS2010 setup projects"
    parser = argparse.ArgumentParser(description=descrip)
    parser.add_argument("-f", "--file", dest="vdproj", action="store", default=None,
            help="The vdproj file to be 'adjusted'", required=True)
    parser.add_argument("-v", "--version", action="store", dest="version", default="1.0.0",
            help="The new version to be set conforming to: major, minor, build e.g '1.0.195'")
    parser.add_argument("-c", "--code", dest="code", action="store", default=str(uuid.uuid4()),
            help="The new product code GUID. If not provided one is generated. ")
    
    ## Don't update the UpgradeCode that needs to stay the same for the product duration

    if test_args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(test_args)
    return args

def main():
    args = parse_commands()
    replace_code_and_version(args.file, args.version, args.code)

if __name__ == '__main__':
    main()
