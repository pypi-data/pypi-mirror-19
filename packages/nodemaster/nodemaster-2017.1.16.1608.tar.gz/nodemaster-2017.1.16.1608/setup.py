#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import setuptools

def main():

    setuptools.setup(
        name             = "nodemaster",
        version          = "2017.01.16.1608",
        description      = "node control utilities",
        long_description = long_description(),
        url              = "https://github.com/wdbm/nodemaster",
        author           = "Will Breaden Madden",
        author_email     = "wbm@protonmail.ch",
        license          = "GPLv3",
        py_modules       = [
                           "nodemaster"
                           ],
        entry_points     = """
            [console_scripts]
            nodemaster = nodemaster:nodemaster
        """
    )

def long_description(
    filename = "README.md"
    ):

    if os.path.isfile(os.path.expandvars(filename)):
        try:
            import pypandoc
            long_description = pypandoc.convert_file(filename, "rst")
        except ImportError:
            long_description = open(filename).read()
    else:
        long_description = ""
    return long_description

if __name__ == "__main__":
    main()
