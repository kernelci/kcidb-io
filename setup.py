#!/usr/bin/env python3
# Copyright (c) 2018 Red Hat, Inc. All rights reserved. This copyrighted
# material is made available to anyone wishing to use, modify, copy, or
# redistribute it subject to the terms and conditions of the GNU General
# Public License v.2 or later.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
"""Install kcidb_io using setuptools."""
import setuptools

with open("README.md", "r", encoding="utf8") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="kcidb_io",
    version="3",
    python_requires=">=3.6",
    author="kernelci.org",
    author_email="kernelci@groups.io",
    description="KCIDB = Linux Kernel CI reporting - I/O data library",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/kernelci/kcidb_io",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GPLv2+",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries",
    ],
    install_requires=[
        "jsonschema[format]",
    ],
    extras_require=dict(
        dev=[
            "flake8",
            "pylint",
            "pytest",
        ],
    ),
)
