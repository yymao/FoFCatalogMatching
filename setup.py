#!/usr/bin/env python
"""
Using friends-of-friends method to iteratively match multiple sky catalogs
without the need of specifying the main catalog.
Project website: https://github.com/yymao/FoFCatalogMatching
The MIT License (MIT)
Copyright (c) 2018 Yao-Yuan Mao (yymao)
http://opensource.org/licenses/MIT
"""
import os
from setuptools import setup

_name = 'FoFCatalogMatching'
_version = ''
with open(os.path.join(os.path.dirname(__file__), '{}.py'.format(_name))) as _f:
    for _l in _f:
        if _l.startswith('__version__ = '):
            _version = _l.partition('=')[2].strip().strip('\'').strip('"')
            break
if not _version:
    raise ValueError('__version__ not define!')

setup(
    name=_name,
    version=_version,
    description='Using friends-of-friends method to iteratively match multiple sky catalogs without the need of specifying the main catalog.',
    url='https://github.com/yymao/{}'.format(_name),
    download_url='https://github.com/yymao/{}/archive/v{}.zip'.format(_name, _version),
    author='Yao-Yuan Mao',
    author_email='yymao.astro@gmail.com',
    maintainer='Yao-Yuan Mao',
    maintainer_email='yymao.astro@gmail.com',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='fof catalog matching merging',
    py_modules=['FoFCatalogMatching'],
    install_requires=['numpy>1.3.0', 'astropy>1.0.0', 'fast3tree>=0.3.1'],
)
