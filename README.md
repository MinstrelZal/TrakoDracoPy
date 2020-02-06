[![PyPI version](https://badge.fury.io/py/DracoPy.svg)](https://badge.fury.io/py/DracoPy)
[![Build Status](https://travis-ci.org/seung-lab/DracoPy.svg?branch=master)](https://travis-ci.org/seung-lab/DracoPy)

# DracoPy

DracoPy is a Python wrapper for Google's Draco mesh compression library

Available as a PyPI package: pip install DracoPy 

DracoPy requires Python >= 3.5, pip >= 10, and a C++ compiler that is fully compatible with C++11.

It supports Linux and OS X.

An example of usage is given in example.py.

** This version is modified from the original https://github.com/seung-lab/DracoPy **

# Setup Toturial

This repo is forked from https://github.com/haehn/TrakoDracoPy and we use the *generic_point_cloud* branch.

To setup the package by yourself (I did these steps to setup):

+ install skbuild by "pip install scikit-build".
+ setup draco
    - git clone draco repo
    - cd draco and modify the CMakeList.txt under the draco dir by adding "option(BUILD_SHARED_LIBS "" ON)" in line (maybe) 58
    - run "mkdir build && cd build && cmake ../ && sudo make install"
+ run "python setup.py build && python setup.py install"