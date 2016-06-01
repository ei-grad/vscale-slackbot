#!/usr/bin/env python

from distutils.core import setup

setup(
    name='vscale-slackbot',
    version='0.1',
    description='Slackbot for vscale.io hosting',
    author='Andrew Grigorev',
    author_email='andrew@ei-grad.ru',
    url='https://github.com/ei-grad/vscale-slackbot',
    py_modules=['vscale_slackbot'],
    entry_points={
        'console_scripts': ['vscale-slackbot=vscale_slackbot:main'],
    },
    install_requires=[
        'slackbot',
        'requests',
    ],
)
