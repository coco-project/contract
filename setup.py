import os
from setuptools import setup, find_packages

setup(
    name="ipynbsrv-contract",
    description="Contract package for various pluggable ipynbsrv components.",
    version="0.0.1",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['ipynbsrv']
)
