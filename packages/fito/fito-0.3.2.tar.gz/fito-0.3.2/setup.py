#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='fito',
    packages=find_packages(),
    version='0.3.2',
    description='fito',
    author='Pablo Zivic',
    author_email='elsonidoq@gmail.com',
    url='https://github.com/elsonidoq/fito',
    download_url='https://github.com/elsonidoq/fito/tarball/0.3.2',
    zip_safe=False,
    install_requires=[
        'mmh3',
        'memoized_property'
    ],
)
