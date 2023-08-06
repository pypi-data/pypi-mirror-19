#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: Jinbo Pan
# Mail: pan.jinbo@outlook.com
# Created Time:  2017-01-06
#############################################


from setuptools import setup, find_packages

setup(
    name = "cnfconverter",
    version = "1.0.2",
    keywords = ("pip", "datacanvas", "cnf", "panjinbo"),
    description = "CNF sdk",
    long_description = "CNF converter sdk for python",

    url = "http://panjinbo.com",
    author = "Jinbo Pan",
    author_email = "pan.jinbo@outlook.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['ply']
)
