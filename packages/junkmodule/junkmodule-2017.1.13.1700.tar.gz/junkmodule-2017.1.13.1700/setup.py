#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import setuptools

def main():

    setuptools.setup(
        name                 = "junkmodule",
        version              = "2017.01.13.1700",
        description          = "junk testing module",
        long_description     = long_description(),
        url                  = "https://github.com/wdbm/junkmodule",
        author               = "Will Breaden Madden",
        author_email         = "wbm@protonmail.ch",
        license              = "GPLv3",
        include_package_data = True,
        py_modules           = [
                               "junkmodule"
                               ],
        install_requires     = [
                               "numpy"
                               ],
        scripts              = [
                               "junkmodule_script.py"
                               ],
        entry_points         = """
            [console_scripts]
            junkmodule = junkmodule:junkmodule
        """
    )

def long_description():

    try:
        try:
            import pypandoc
            long_description = pypandoc.convert("README.md", "rst")
        except ImportError:
            long_description = open("README.md").read()
    except Exception:
        long_description = ""
    return long_description

if __name__ == "__main__":
    main()
