# -*- coding: utf-8 -*-
"""
vsgen's setup.py

For more details see https://packaging.python.org/en/latest/distributing/#setup-args
"""
from os import path
from sys import version_info
from setuptools import setup, find_packages
from codecs import open

ROOT_PATH = path.abspath(path.dirname(__file__))

if version_info < (3,):
    INSTALL_REQUIREMENTS = ['jinja2', 'configparser']
else:
    INSTALL_REQUIREMENTS = ['jinja2']

TEST_REQUIREMENTS = [
    'pep8'
]

# Pre-install pylint in Python 3 at 1.6.5 as a
# work around for https://github.com/dbarsam/python-vsgen/issues/14
if version_info[0] == 3:
    SETUP_REQUIREMENTS = [
        'pylint==1.6.5'
    ]
else:
    SETUP_REQUIREMENTS = []

SETUP_REQUIREMENTS += [
    'setuptools-pep8',
    'setuptools-lint',
    'setuptools_scm'
]

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Topic :: Software Development ',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.6',
    'Topic :: Office/Business :: Groupware',
]

ENTRY_POINTS = {
    'console_scripts': [
        'vsgen = vsgen.__main__:main'
    ]
}

PACKAGES = find_packages(exclude=['contrib', 'docs', 'tests', '.eggs'])

README = open(path.join(ROOT_PATH, 'README.rst'), encoding='utf-8').read()

CHANGES = open(path.join(ROOT_PATH, 'CHANGES.rst'), encoding='utf-8').read()

LONG_DESCRIPTION = README + '\n\n' + CHANGES

PACKAGE_DIR = {
    'vsgen': './vsgen'
}

PACKAGE_DATA = {
    'vsgen': ['data/*.*']
}

SCM_VERSION = {
    'local_scheme': 'dirty-tag'
}

setup(
    name='vsgen',
    description='A Microsoft Visual Studio solution and project generator pyackage.',
    long_description=LONG_DESCRIPTION,
    url='https://github.com/dbarsam/python-vsgen',
    author='dbarsam',
    author_email='dbarsam@gmail.com',
    license='MIT',
    setup_requires=SETUP_REQUIREMENTS,
    classifiers=CLASSIFIERS,
    keywords='visual studio project generation',
    packages=PACKAGES,
    package_dir=PACKAGE_DIR,
    package_data=PACKAGE_DATA,
    test_suite='tests',
    tests_require=TEST_REQUIREMENTS,
    entry_points=ENTRY_POINTS,
    install_requires=INSTALL_REQUIREMENTS,
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
    use_scm_version=SCM_VERSION
)
