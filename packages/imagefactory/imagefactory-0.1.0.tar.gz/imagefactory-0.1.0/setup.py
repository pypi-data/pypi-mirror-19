#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()


requirements = [
    'click',
    'Pillow',
]

extras_require = {
    'SVG': ['svgwrite']
}

test_requirements = [
    'pytest',
    'coverage',
    'pytest-cov',
    'hypothesis',
]

setup(
    name='imagefactory',
    version='0.1.0',
    description="Python package for creating test images.",
    long_description=readme + '\n\n' + history,
    author="Jaan Tollander de Balsch",
    author_email='jaan.tollander@gmail.com',
    url='https://github.com/jaantollander/imagefactory',
    packages=[
        'imagefactory',
    ],
    package_dir={'imagefactory':
                 'imagefactory'},
    entry_points={
        'console_scripts': [
            'imagefactory=imagefactory.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    extras_require=extras_require,
    license="MIT license",
    zip_safe=False,
    keywords='imagefactory',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.6',
        # 'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
