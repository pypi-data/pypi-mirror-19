import os
import sys

from setuptools import setup, find_packages

setup(
    name='autobi',
    version='0.0.0',
    description='Namespace package for AutoBI releases',

    author="AutoBI",
    maintainer_email='chriscz93@gmail.com',

    packages=find_packages(),

    classifiers=[
        "Programming Language :: Python :: 3.5",
    ]
)
