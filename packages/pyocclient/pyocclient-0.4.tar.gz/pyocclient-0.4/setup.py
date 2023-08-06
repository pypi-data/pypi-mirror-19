# -*- coding: utf-8 -*-
#
# vim: expandtab shiftwidth=4 softtabstop=4
#
from setuptools import setup

version = '0.4'

long_description = (
    open('README.rst').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('docs/source/CONTRIBUTORS.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')

setup(
    name='pyocclient',
    version=version,
    author='Vincent Petry',
    author_email='pvince81@owncloud.com',
    packages=['owncloud', 'owncloud.test'],
    url='https://github.com/owncloud/pyocclient/',
    license='LICENSE.txt',
    description='Python client library for ownCloud',
    long_description=long_description,
    install_requires=[
        "requests >= 2.0.1",
        "six"
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License'
    ]
)
