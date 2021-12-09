#!/usr/bin/env python3
from setuptools import setup

setup(
    name="binex-futures",
    version="0.1.0",
    packages=['binex_f'],
    install_requires=['requests', 'urllib3', 'websocket-client']
)
