# setup.py
# Copyright (c) 2015-2017 Arkadiusz Bokowy
#
# This file is a part of pyexec.
#
# This project is licensed under the terms of the MIT license.

from setuptools import setup

import pyexec


with open("README.rst") as f:
    long_description = f.read()

setup(
    name="pyexec",
    version=pyexec.__version__,
    author="Arkadiusz Bokowy",
    author_email="arkadiusz.bokowy@gmail.com",
    url="https://github.com/Arkq/pyexec",
    description="Signal-triggered process reloader",
    long_description=long_description,
    license="MIT",
    py_modules=["pyexec"],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
)
