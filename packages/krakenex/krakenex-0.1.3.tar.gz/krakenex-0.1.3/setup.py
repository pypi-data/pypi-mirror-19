#!/usr/bin/env python3

from distutils.core import setup

exec(open('./krakenex/version.py').read())

setup(name='krakenex',
      version=__version__,
      description='kraken.com cryptocurrency exchange API',
      author='Noel Maersk',
      author_email='veox+packages+spamremove@veox.pw',
      url=__url__,
      packages=['krakenex'],
      classifiers=[
          'Programming Language :: Python :: 3',
      ],
)
