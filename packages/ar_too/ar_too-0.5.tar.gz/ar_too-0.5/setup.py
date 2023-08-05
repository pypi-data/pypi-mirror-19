#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    "click",
    "requests",
    "xmltodict"
]

test_requirements = [
    "click",
    "mock",
    "pytest",
    "xmltodict"
]

setup_requirements = []

setup(
    name='ar_too',
    version="0.5",
    use_scm_version=True,
    setup_requires=setup_requirements,
    description="Artifactory configuration tool",
    long_description=readme,
    author="MCP CI",
    author_email='mcp-ci@mirantis.com',
    url='https://github.com/brain461/ar_too.git',
    download_url = 'https://github.com/brain461/ar_too/tarball/0.4',
    packages=['ar_too'],
    package_dir={'ar_too':
                 'ar_too'},
    include_package_data=True,
    install_requires=requirements,
    license="Apache",
    zip_safe=False,
    keywords='ar_too',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
        'console_scripts': ['ar_too=ar_too.cli:cli']
    }
)
