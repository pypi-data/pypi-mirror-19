#!/usr/bin/env python

import os
from setuptools import setup, find_packages

setup(
    name="logshuttle",
    version="0.2.2",
    url="https://github.com/arunbala/logshuttle/",
    license=open("LICENSE").read(),
    author="Arun Bala",
    author_email="arunprakashb@gmail.com",
    description="Python 3 log handler for sending log records to Google Cloud Stackdriver service as custom logs in batches.",
    install_requires=['google-cloud >= 0.22.0'],
    tests_require=[],
    extras_require={'test': []},
    packages=find_packages(exclude=["test"]),
    platforms=["MacOS X", "Posix"],
    include_package_data=True,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
