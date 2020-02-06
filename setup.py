# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

os.system('pip install git+https://github.com/RealVNF/coordination-simulation.git')

requirements = [
    'numpy',
    'networkx',
    'PyYAML',
    'coord-sim'
]

test_requirements = [
    'flake8',
    'nose2'
]

dev_requirements = []

setup(
    name='coord-interface',
    version='0.0.2',
    description="Interface definition between coordination algorithms and environments. "
                "Includes Non-RL algorithms and environment as example.",
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
            "rs=algorithms.randomSchedule:main",
            "lb=algorithms.loadBalance:main",
            "sp=algorithms.shortestPath:main"
        ],
    },
)
