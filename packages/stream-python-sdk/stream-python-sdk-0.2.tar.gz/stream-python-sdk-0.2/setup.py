# -*- coding: utf-8 -*-

from os.path import join, dirname
from setuptools import setup, find_packages
import sys
import re

version = ""
with open("stream/client/utils.py", "r") as fd:
    version = re.search(r"^VERSION\s*=\s*[\"']([^\"']*)[\"']", fd.read(),
                        re.MULTILINE).group(1)

long_description = ""
with open(join(dirname(__file__), "README.rst")) as fd:
    long_description = fd.read().strip()

install_requires = [
    "urllib3>=1.8, <2.0",
    "certifi",
]

# use external unittest for 2.6
if sys.version_info[:2] == (2, 6):
    install_requires.append("unittest2")

setup(
    name="stream-python-sdk",
    description="Stream SDK",
    license="MIT License",
    url="https://github.com/NetEase-Cloudsearch/stream-python-sdk",
    long_description=long_description,
    version=version,
    author="Stream Developer",
    author_email="hzhuangzhenxi@corp.netease.com",
    packages=find_packages(
        where=".",
        exclude=("test_stream*",)
    ),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7"
    ],
    install_requires=install_requires
)
