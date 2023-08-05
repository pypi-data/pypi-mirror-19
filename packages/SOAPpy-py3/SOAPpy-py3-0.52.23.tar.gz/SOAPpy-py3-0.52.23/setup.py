#!/usr/bin/env python
#
# $Id: setup.py,v 1.11 2005/02/15 16:32:22 warnes Exp $

CVS = 0

import os

from setuptools import setup, find_packages


def read(*rnames):
    return "\n" + open(
        os.path.join('.', *rnames)
    ).read()


url = "https://github.com/Synerty/SOAPpy-py3"
long_description = "SOAPpy-py3 provides tools for building SOAP clients and servers.  For more information see " + url \
                   + '\n' + read('README.txt') \
                   + '\n' + read('CHANGES.txt')
setup(
    name="SOAPpy-py3",
    version='0.52.23',  # Add 0.40.0 for the SOAPpy-py3 port
    description="SOAP Services for Python",
    maintainer="Synerty",
    maintainer_email="contact@synerty.com",
    url=url,
    long_description=long_description,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'wstools',
        'defusedxml',
    ]
)
