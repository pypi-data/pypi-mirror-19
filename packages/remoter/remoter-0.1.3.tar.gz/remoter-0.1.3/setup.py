#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'paramiko>=2.0',
    'PyYAML>=3.0'
]

test_requirements = [
    'flake8>= 3.2.1',
    'coverage>=4.3.4',
    'pytest>=3.0.0'
]

setup(
    name='remoter',
    version='0.1.3',
    description="Python 3 compatible remote task runner",
    long_description=readme + '\n\n' + history,
    author="Lev Rubel",
    author_email='rubel.lev@gmail.com',
    url='https://github.com/levchik/remoter',
    packages=[
        'remoter',
    ],
    package_dir={'remoter':
                 'remoter'},
    entry_points={
        'console_scripts': [
            'remoter=remoter.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='remoter,remote,ssh,update,deploy',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    cmdclass={'test': PyTest},
    test_suite='tests',
    tests_require=test_requirements
)
