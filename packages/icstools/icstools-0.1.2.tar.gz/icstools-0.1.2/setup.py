#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='icstools',
    version='0.1.2',
    description='cat/grep-like for icalendar calendar files (.ics)',
    long_description=open('README.md').read(),
    author='Jocelyn Delalande',
    author_email='jocelyn@crapouillou.net',
    url='https://code.crapouillou.net/jocelyn/icstools',
    install_requires=[
        'icalendar>=3',
    ],
    packages=find_packages(),
    include_package_data=True,

    entry_points = {
        'console_scripts': [
            'icsgrep = icstools.icsgrep:main',
            'icscat = icstools.icscat:main',
        ]
    },
    classifiers= [
        'Topic :: Office/Business :: Scheduling',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    ]
)
