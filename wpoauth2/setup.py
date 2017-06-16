#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

version = '0.2.0'

setup(
    name='wp-oauth2',
    version=version,
    description='Open Authentication 2 support to Python-requests HTTP library. Includes client grants and tokens.',
    long_description=open('README.md').read(),
    author='BCBud.store with original code by Miguel Araujo',
    author_email='webmaster@bcbud.store',
    url='https://github.com/bcbudstore/wp-api-python',
    packages=find_packages(),
    install_requires=['requests', ],
    license='BSD',
    # classifiers=(
    #     "Development Status :: 5 - Production/Stable",
    #     'Intended Audience :: Developers',
    #     'Programming Language :: Python',
    #     "License :: OSI Approved :: BSD License",
    #     "Operating System :: OS Independent",
    #     "Topic :: Internet :: WWW/HTTP",
    #     "Topic :: Software Development :: Libraries :: Python Modules",
    # ),
    # keywords=['requests', 'python-requests', 'OAuth', 'open authentication'],
    zip_safe=False,
)
