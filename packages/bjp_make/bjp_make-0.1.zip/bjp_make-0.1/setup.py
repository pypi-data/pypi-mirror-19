#! /usr/bin/env python

from setuptools import setup

setup(name              = 'bjp_make',
      version           = '0.1',
      description       = 'Wrapping code for project execution.',
      long_description  = open('README.md').read(),
      classifiers       = [
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
      ],
      url               = 'https://github.com/bperry12/bjp_python/tree/master/bjp_make',
      author            = 'Bryan J. Perry',
      author_email      = 'perryb@mit.edu',
      license           = 'MIT',
      packages          = ['bjp_make'],
      install_requires  = [],
      zip_safe          = True)