#!/usr/bin/env python
import re
import io
import codecs

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class NoseTestCommand(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # Run nose ensuring that argv simulates running nosetests directly
        import nose
        nose.run_exit(argv=['nosetests'])


setup(
    name = 'team_password_cli',
    description = 'Team Password Manager cli',
    version = re.search(r'''^__version__\s*=\s*["'](.*)["']''', open('team_password_cli/__init__.py').read(), re.M).group(1),
    author = 'Nico Di Rocco',
    author_email = 'dirocco.nico@gmail.com',
    url = 'https://github.com/nrocco/team_password_cli',
    license = 'GPLv3',
    long_description = codecs.open('README.rst', 'rb', 'utf-8').read(),
    test_suite = 'nose.collector',
    download_url = 'https://github.com/nrocco/team_password_cli/tags',
    include_package_data = True,
    install_requires = [
        'pycli-tools',
        'requests',
        'tabulate',
    ],
    tests_require = [
        'nose',
        'mock',
        'coverage',
    ],
    entry_points = {
        'console_scripts': [
            'passctl = team_password_cli.command:parse_and_run',
        ]
    },
    packages = find_packages(),
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
    cmdclass = {
        'test': NoseTestCommand
    }
)
