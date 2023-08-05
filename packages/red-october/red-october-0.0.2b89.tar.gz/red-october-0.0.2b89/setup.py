# -*- coding: utf-8 -*-
# Copyright 2016-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

from setuptools import Command, setup
from setuptools import find_packages
from unittest import TestLoader, TextTestRunner

from os import environ, path

version = environ.get('RELEASE') or environ.get('VERSION') or '0.0.0'

if environ.get('TRAVIS_BUILD_NUMBER'):
    version += 'b%s' % environ.get('TRAVIS_BUILD_NUMBER')


setup_vals = {
    'name': 'red-october',
    'author': 'LasLabs Inc.',
    'author_email': 'support@laslabs.com',
    'description': 'This library will allow you to interact with Red October '
                   'using Python.',
    'url': 'https://laslabs.github.io/python-red-october',
    'download_url': 'https://github.com/LasLabs/python-red-october',
    'license': 'MIT',
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    'version': version,
}


if path.exists('README.rst'):
    with open('README.rst') as fh:
        setup_vals['long_description'] = fh.read()


class FailTestException(Exception):
    """ It provides a failing build """
    pass


class Tests(Command):
    ''' Run test & coverage, save reports as XML '''

    MODULE_NAMES = [
        'red-october',
    ]
    user_options = []  # < For Command API compatibility

    def initialize_options(self, ):
        pass

    def finalize_options(self, ):
        pass

    def run(self, ):
        loader = TestLoader()
        tests = loader.discover('.', 'test_*.py')
        t = TextTestRunner(verbosity=1)
        res = t.run(tests)
        if not res.wasSuccessful():
            raise FailTestException()

if __name__ == "__main__":
    setup(
        packages=find_packages(exclude=('tests')),
        cmdclass={'test': Tests},
        tests_require=[
            'mock',
        ],
        install_requires=[
            'enum34',
            'requests',
        ],
        **setup_vals
    )

