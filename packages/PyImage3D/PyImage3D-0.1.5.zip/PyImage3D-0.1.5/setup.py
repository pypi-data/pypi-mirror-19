#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PyImage3D
from os.path import exists
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
  name="PyImage3D",
  packages=["PyImage3D"],
  version="0.1.5",
  description="PyImage3D is a Python port of the PHP's Image3D library.",
  author=u"Primož 'Naltharial' Jeras",
  author_email="primoz.jeras@offblast.si",
  url="https://bitbucket.org/Naltharial/pyimage3d",
  download_url="https://bitbucket.org/Naltharial/pyimage3d/get/0.1.tar.gz",
  keywords=['3d', 'image', 'render'],
  classifiers=[],
  include_package_data=True,
)
