#!/usr/bin/env python

from setuptools import setup

setup(
    name="cine",
    version="0.1",
    author="Miguel de Val-Borro",
    author_email="miguel.deval@gmail.com",
    url="https://github.com/migueldvb/chirp",
    packages=["chirp"],
    description="Calculate infrared pumping rates by solar radiation",
    long_description=open("README.md").read(),
    package_data={"": ["LICENSE"]},
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
    ],
)
