#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='unique_id_gen',
    version='0.1.0',
    description="A package that generates unique randomized ids",
    long_description=readme + '\n\n' + history,
    author="Michael Navazhylau",
    author_email='mikipux7@gmail.com',
    url='https://github.com/mechasparrow/unique_id_gen',
    packages=[
        'unique_id_gen',
    ],
    package_dir={'unique_id_gen':
                 'unique_id_gen'},
    entry_points={
        'console_scripts': [
            'unique_id_gen=unique_id_gen.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='unique_id_gen',
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
    test_suite='tests',
    tests_require=test_requirements
)
