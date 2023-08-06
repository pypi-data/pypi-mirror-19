#
# setup.py
#
# Copyright (c) 2017 Junpei Kawamoto
#
# This file is part of rgmining-tripadvisor-dataset.
#
# rgmining-tripadvisor-dataset is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# rgmining-tripadvisor-dataset is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#
# pylint: disable=invalid-name
"""Package information about a synthetic dataset for review graph mining.
"""
import distutils.command.install_data
from os import path
from setuptools import setup
import urllib


class CustomInstallData(distutils.command.install_data.install_data):
    """Custom install data command to download data files from the web.
    """
    def run(self):
        """Before executing run command, download data files.
        """
        for f in self.data_files:
            if not isinstance(f, tuple):
                continue
            for i, u in enumerate(f[1]):
                f[1][i] = urllib.urlretrieve(u, path.basename(u))[0]
        return distutils.command.install_data.install_data.run(self)


def _load_requires_from_file(filepath):
    """Read a package list from a given file path.

    Args:
      filepath: file path of the package list.

    Returns:
      a list of package names.
    """
    with open(filepath) as fp:
        return [pkg_name.strip() for pkg_name in fp.readlines()]


setup(
    name="rgmining-tripadvisor-dataset",
    version="0.5.3",
    author="Junpei Kawamoto",
    author_email="kawamoto.junpei@gmail.com",
    description="Trip Advisor dataset for Review Graph Mining Project",
    url="https://github.com/rgmining/tripadvisor",
    py_modules=[
        "tripadvisor"
    ],
    install_requires=_load_requires_from_file("requirements.txt"),
    data_files=[(
        "rgmining/data",
        ["http://times.cs.uiuc.edu/~wang296/Data/LARA/TripAdvisor/TripAdvisorJson.tar.bz2"]
    )],
    test_suite="tests.suite",
    license="GPLv3",
    cmdclass={
        "install_data": CustomInstallData
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries",
        "Topic :: Scientific/Engineering :: Information Analysis"
    ]
)
