#!/usr/bin/env python

import os

from setuptools import setup, find_packages

import versioneer

BASE_DIR = os.path.dirname(__file__)
LICENSE_PATH = os.path.join(BASE_DIR, 'LICENSE')
LICENSE = open(LICENSE_PATH).readline().strip()

setup(
    name='updatable_zipfile',
    version=versioneer.get_version(),
    description='Updatable Zip File',
    author='Mars Galactic',
    author_email='xoviat@users.noreply.github.com',
    url='https://github.com/xoviat/updatable_zipfile',
    packages=find_packages(),
    license=LICENSE,
    platforms='any',
    keywords=['zipfile'],
    classifiers=[],
    cmdclass=versioneer.get_cmdclass(),
    setup_requires=['setuptools-markdown'],
    long_description_markdown_filename='README.md')
