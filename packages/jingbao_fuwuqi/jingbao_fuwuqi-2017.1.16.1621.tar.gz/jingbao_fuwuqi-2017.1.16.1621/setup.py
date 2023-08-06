#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import setuptools
import pypandoc

def main():

    setuptools.setup(
        name             = "jingbao_fuwuqi",
        version          = "2017.01.16.1621",
        description      = "alert when server available",
        long_description = long_description(),
        url              = "https://github.com/wdbm/jingbao-fuwuqi",
        author           = "Will Breaden Madden",
        author_email     = "wbm@protonmail.ch",
        license          = "GPLv3",
        py_modules       = [
                           "jingbao_fuwuqi"
                           ],
        install_requires = [
                           "bs4",
                           "docopt"
                           ],
        scripts          = [
                           "jingbao_fuwuqi.py"
                           ],
        entry_points     = """
            [console_scripts]
            jingbao_fuwuqi = jingbao_fuwuqi:jingbao_fuwuqi
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
