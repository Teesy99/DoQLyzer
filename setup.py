#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="dohlyzer",
    description="Set of tools to capture HTTPS traffic, extract statistical and time-series features from it, and analyze them with a focus on detecting and characterizing DoH (DNS-over-HTTPS) traffic.  ",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ahlashkari/DoHlyzer",
    packages=find_packages(exclude=[]),
    python_requires=">=3.6",
    install_requires=open('requirements.txt').read().split('\n'),
    entry_points={
        "console_scripts": [
            "dohlyzer=meter.dohlyzer:main",
        ]
    },
)
