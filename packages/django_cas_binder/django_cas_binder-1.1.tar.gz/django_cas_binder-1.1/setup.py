#!/usr/bin/env python

import os.path
#THIS_DIR = os.path.dirname(os.path.abspath(__file__))
#os.chdir(os.path.dirname(THIS_DIR))

from distutils.core import setup


setup(
    name='django_cas_binder',
    version='1.1',
    description='A thin wrapper around django-cas-ng that allows to use identifier other than "username".',  # NOQA
    author='',
    author_email='',
    url='',
    packages=['django_cas_binder'],
)
