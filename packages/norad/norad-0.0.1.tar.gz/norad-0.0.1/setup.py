#!/usr/bin/env python
"""
Setup script for Norad's Python SDK.
"""
from setuptools import setup

setup(
    name='norad',
    version='0.0.1',
    description='Python SDK for Norad',
    author='David Wyde',
    author_email='dwyde@cisco.com',
    url='https://norad-gitlab.cisco.com/norad/python-sdk/',
    packages=['norad'],
    install_requires=['requests >= 2.10.0'],
)
