#!/usr/bin/env python

from distutils.core import setup

setup(name='fito',
      packages=['fito'],
      version='0.1',
      description='fito',
      author='Pablo Zivic & Bruno Parrino',
      author_email='elsonidoq@gmail.com',
      url='https://github.com/elsonidoq/fito',
      download_url='https://github.com/elsonidoq/fito/tarball/0.1',
      install_requires=[
            'mmh3',
            'memoized_property'
      ],
     )
