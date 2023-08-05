# -*- coding: utf-8 -*-
import os
import re
from setuptools import find_packages, setup


setup(
    name='mytsgraph',
    version='1.0.0',
    description='MySQL table space monitoring.',
    long_description=open('README.md').read(),
    author=u'Jérémy Cohen Solal',
    author_email='jeremy.cohen-solal@dalenys.com',
    url='https://github.com/dalenys/mytsgraph',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'mysql-python',
        'mock'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Database :: Database Engines/Servers',
        'Topic :: System :: Monitoring',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts': [
            'mytsgraph = mytsgraph:main',
        ],
    },
    test_suite="tests",
)
