#!/usr/bin/env python
# -----------------------------------------------------------------------------
# Copyright (c) Gonzalo Peña-Castellanos (@goanpeca)
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Setup script for pyzenhub."""
import ast
import os

from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))


def get_version(module="zenhub"):
    """Get version."""
    with open(os.path.join(HERE, module, "__init__.py")) as f:
        data = f.read()

    lines = data.split("\n")
    for line in lines:
        if line.startswith("__version__"):
            version = ast.literal_eval(line.split("=")[-1].strip())
            break

    return version


def get_description() -> str:
    """Get long description."""
    with open(os.path.join(HERE, "README.md")) as f:
        data = f.read()
    return data


REQUIREMENTS = ["requests", "typing_extensions", "types-requests"]

setup(
    name="pyzenhub",
    version=get_version(),
    keywords=["zenhub api"],
    url="https://github.com/goanpeca/pyzenhub",
    license="MIT",
    author="Gonzalo Pena-Castellanos",
    author_email="goanpeca@gmail.com",
    maintainer="Gonzalo Pena-Castellanos",
    maintainer_email="goanpeca@gmail.com",
    description="Python bindings to the Zenhub API",
    long_description=get_description(),
    long_description_content_type="text/markdown",
    packages=["zenhub"],
    include_package_data=True,
    install_requires=REQUIREMENTS,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
