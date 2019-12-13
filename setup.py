# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

requirements = [
    'numpy',
    'networkx',
    'PyYAML'
]

test_requirements = [
    'flake8',
    'nose2'
]

dev_requirements = []

setup(
    name='coord-interface',
    version='0.0.1',
    description="Interface definition between coordination algorithms and environments. "
                "Includes a dummy algorithm and environment as example.",
    url='https://github.com/RealVNF/coord-interface',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=requirements + test_requirements,
    tests_require=test_requirements,
    extras_require={
        'dev': dev_requirements
    },
    test_suite='nose2.collector.collector',
    zip_safe=False,
    entry_points={
        'console_scripts': [
            "dummy-coord=dummy_algo.coordinator:main"
        ],
    },
)
