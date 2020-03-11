# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


requirements = [
    'networkx',
    'PyYAML',
    'numpy'
]

test_requirements = [
    'flake8'
]


setup(
    name='common-utils',
    version='0.1.0',
    description="Interface definition between coordination algorithms and environments. "
                "Includes a dummy environment.",
    url='https://github.com/RealVNF/common-utils',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=requirements + test_requirements,
    tests_require=test_requirements,
    zip_safe=False,
)
