#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pypandoc
import setuptools

def main():

    setuptools.setup(
        name                 = "tonescale",
        version              = "2017.01.13.1331",
        description          = "sound utilities and sounds",
        long_description     = pypandoc.convert("README.md", "rst"),
        url                  = "https://github.com/wdbm/tonescale",
        author               = "Will Breaden Madden",
        author_email         = "wbm@protonmail.ch",
        license              = "GPLv3",
        include_package_data = True,
        py_modules           = [
                               "tonescale"
                               ],
        install_requires     = [
                               "numpy",
                               "scipy",
                               "shijian"
                               ],
        scripts              = [
                               "sound_search.py"
                               ],
        entry_points         = """
            [console_scripts]
            tonescale = tonescale:tonescale
        """
    )

def read(*paths):
    with open(os.path.join(*paths), "r") as filename:
        return filename.read()

if __name__ == "__main__":
    main()
