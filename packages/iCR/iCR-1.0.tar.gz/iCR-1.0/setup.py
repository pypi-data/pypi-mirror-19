#!/usr/bin/env python
from setuptools import setup, find_packages
setup(
        name="iCR",
        version="1.0",
        packages=find_packages(),
        scripts=['iCR.py'],
        install_requires=['json>=2.0.7'],
        author="Pete White",
        author_email="pwhite@f5.com",
        description="This is a Python module to easily use the F5 iControl REST interface",
        license="PSF",
)
