# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

os.system('pip install git+https://github.com/RealVNF/coord-env-interface.git')
os.system('pip install git+https://github.com/RealVNF/coordination-simulation.git')

requirements = [
    'networkx',
    'PyYAML',
]

test_requirements = [
    'flake8',
    'nose2'
]


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
    zip_safe=False,
    entry_points={
        'console_scripts': [
            "rs=algorithms.randomSchedule:main",
            "lb=algorithms.loadBalance:main",
            "sp=algorithms.shortestPath:main"
        ],
    },
)
