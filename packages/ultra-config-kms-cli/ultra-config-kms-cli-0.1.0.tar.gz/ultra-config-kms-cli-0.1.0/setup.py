#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'ultra-config[aws]>=0.6.2',
    'boto3'
]

test_requirements = [
    'pylint'
]

setup(
    name='ultra-config-kms-cli',
    version='0.1.0',
    description="A simple cli package for easily updating ECS task definition files with secrets",
    long_description=readme + '\n\n' + history,
    author="Apptimize (Tim Martin)",
    author_email='engineering@apptimize.com',
    url='https://github.com/Apptimize-OSS/ultra-config-kms-cli',
    py_modules=['ultra_config_kms_cli'],
    entry_points={
        'console_scripts': [
            'ultra_config_kms_cli=ultra_config_kms_cli.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='ultra_config_kms_cli',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='ultra_config_kms_cli_tests',
    tests_require=test_requirements
)
