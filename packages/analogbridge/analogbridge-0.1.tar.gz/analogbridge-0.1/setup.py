import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py

install_requires = ['requests >= 0.8.8']

setup(
    name='analogbridge',
    cmdclass={'build_py': build_py},
    version='0.1',
    description='Analog Bridge Python bindings',
    long_description='Enable users to import any analog media format directly into your app with the Analog Bridge API',
    author='Eugene Gekhter',
    author_email='support@analogbridge.io',
    url='https://github.com/analogbridge/analog-bridge-python',
    packages=['analogbridge'],
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ])
