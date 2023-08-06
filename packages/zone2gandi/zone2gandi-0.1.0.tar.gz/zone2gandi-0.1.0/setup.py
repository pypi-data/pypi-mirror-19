# -*- coding: utf-8 -*-

"""setup.py: setuptools control."""

import re
from setuptools import setup

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('zone2gandi/zone2gandi.py').read(),
    re.M
    ).group(1)


with open('README.rst', 'rb') as f:
    long_descr = f.read().decode('utf-8')

setup(
    name = 'zone2gandi',
    packages = ['zone2gandi'],
    install_requires=[
      'PyYAML', 'json2yaml',
    ],
    entry_points = {
        'console_scripts': ['zone2gandi = zone2gandi.zone2gandi:main']
        },
    version = version,
    description = 'Utility to push zone files up to Gandi DNS.',
    long_description = long_descr,
    author = 'Kevin Lyda',
    author_email = 'kevin@ie.suberic.net',
    url = 'https://gitlab.com/lyda/zone2gandi',
    )
