#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Setup file for numdifftools.

    This file was generated with PyScaffold 2.4.2, a tool that easily
    puts up a scaffold for your new Python project. Learn more under:
    http://pyscaffold.readthedocs.org/

Usage:
Run all tests:
  python setup.py test

  python setup.py doctests

Build documentation

  python setup.py docs

Install
  python setup.py install [, --prefix=$PREFIX]

Build

  python setup.py bdist_wininst

  python setup.py bdist_wheel --universal

  python setup.py sdist


PyPi upload:
  git pull origin
  git tag v0.9.16 master
  git shortlog v0.9.15..v0.9.16 > log.txt  # update Changes.rst
  git commit
  git tag v0.9.17 master
  python setup.py sdist
  python setup.py bdist_wheel --universal
  python setup.py egg_info
  git push --tags
  twine -p PASSWORD upload dist/*
"""

import sys
from setuptools import setup

def print_version():
    import pkg_resources
    try:
        __version__ = pkg_resources.get_distribution("numdifftools").version
        with open("__conda_version__.txt","w") as fid:
            fid.write(__version__)
    except pkg_resources.DistributionNotFound:
        __version__ = 'unknown'
    print("Version: {}".format(__version__))


def setup_package():
    needs_sphinx = {'build_sphinx', 'upload_docs'}.intersection(sys.argv)
    sphinx = ['sphinx', 'numpydoc', 'sphinx_rtd_theme>=0.1.7'] if needs_sphinx else []
    setup(setup_requires=['six', 'pyscaffold>=2.4rc1,<2.5a0'] + sphinx,
          tests_require=['pytest_cov', 'pytest', 'hypothesis', 'matplotlib'],
          use_pyscaffold=True)
    print_version()


if __name__ == "__main__":
    setup_package()
