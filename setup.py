#!/usr/bin/env python3
from setuptools import setup

setup(
    name="binex_f",
    version="0.1.1",
    author='DeepLn',
    author_email='keyjunze@gmail.com',
    url='https://github.com/DeepLn/binex_f.git',
    description='An unofficial Python wrapper for the Binance exchange REST API',
    packages=['binex_f', 'binex_f.ws'],
    install_requires=['requests', 'urllib3', 'websocket-client']
)
