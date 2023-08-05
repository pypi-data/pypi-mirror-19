#!/usr/bin/env python
from setuptools import setup, find_packages
import re


with open('README.rst') as f:
    readme = f.read()


with open('record_ip_to_dnspod/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

setup(
    name='record-ip-to-dnspod',
    version=version,
    description='Record IP Via DNSPod API.',
    long_description=readme,
    author='codeif',
    author_email='me@codeif.com',
    url='https://github.com/codeif/record-ip-to-dnspod',
    license='MIT',
    entry_points={
        'console_scripts': [
            'record-ip-to-dnspod = record_ip_to_dnspod.bin:main',
        ],
    },
    packages=find_packages(exclude=("tests", "tests.*")),
)
