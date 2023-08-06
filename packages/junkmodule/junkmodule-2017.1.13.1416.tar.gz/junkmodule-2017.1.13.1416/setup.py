#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pypandoc
import setuptools

def main():

    setuptools.setup(
        name                 = "junkmodule",
        version              = "2017.01.13.1416",
        description          = "junk testing module",
        long_description     = pypandoc.convert("README.md", "rst"),
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

if __name__ == "__main__":
    main()
