# coding=utf-8
import os

from setuptools import find_packages, setup

with open('README.rst') as readme:
    long_description = readme.read()

setup(
    name = "manipulator",
    version = "0.0.2",
    description = "Python data manipulation made braindead",
    long_description = long_description,
    author = "Veit Heller",
    author_email = "veit@veitheller.de",
    license = "MIT License",
    url = "https://github.com/hellerve/manipulator",
    download_url = 'https://github.com/hellerve/hawkweed/tarball/0.0.2',
    packages = find_packages(),
    include_package_data = True,
)
