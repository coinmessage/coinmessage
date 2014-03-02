#!/usr/bin/env python

import sys
from setuptools import setup


install_requires = [
    'pycrypto >=2.6',
    'pycoin >=0.23',
    ]

setup(
    name='coinmessage',
    version=0.1,
    description='Secure Messaging with Bitcoin and Altcoin Addresses',
    author='Jimmy Song',
    author_email='jaejoon@gmail.com',
    url='http://coinmessage.com',
    packages=['coinmessage', 'coinmessage.tests'],
    install_requires=install_requires,
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Security',
        'Programming Language :: Python',
        ],
    test_suite='coinmessage.tests',
    ),
