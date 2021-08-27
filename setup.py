#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os.path
from setuptools import setup, find_packages

script_path = os.path.dirname(__file__)

setup(
    name='cyclonedx-python-lib',
    version=open(os.path.join(script_path, 'VERSION')).read(),
    url="https://github.com/sonatype-nexus-community/cyclonedx-python-lib",
    author="Sonatype Community",
    author_email="community-group@sonatype.com",
    description="A library for producing CycloneDX SBOM (Software Bill of Materials) files.",
    long_description=open(os.path.join(script_path, 'README.md')).read(),
    long_description_content_type="text/markdown",
    keywords=["BOM", "SBOM", "SCA", "OWASP"],
    license="Apache-2.0",
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Legal Industry',
        'Intended Audience :: System Administrators',
        'Topic :: Security',
        'Topic :: Software Development',
        'Topic :: System :: Software Distribution',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3'
    ],
    packages=find_packages(),
    python_requires='>=3.6',
    package_data={
        'cyclonedx': ['schema/*.json', 'schema/*.xsd', 'schema/ext/*.json', 'schema/ext/*.xsd']
    },
    include_package_data=True,
    install_requires=open(os.path.join(script_path, 'requirements.txt')).read()
)
