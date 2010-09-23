# -*- coding: utf8 -*-

# License: bsd license. 
# See 'license.txt' for more informations.

from distutils.core import setup
import os
import pymagnolia

setup(
    name='pymagnolia',
    version=pymagnolia.VERSION,
    author=pymagnolia.AUTHOR,
    author_email=pymagnolia.AUTHOR_EMAIL,
    url=pymagnolia.PROJECT_URL,
    description=pymagnolia.DESCRIPTION,
    long_description=pymagnolia.LONG_DESCRIPTION,
    py_modules=['pymagnolia'],
    )

