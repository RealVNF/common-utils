# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


requirements = [
    'networkx==2.4',
    'PyYAML',
    'numpy>=1.16.5,<1.19'
]

test_requirements = [
    'flake8'
]


setup(
    name='common-utils',
    version='1.0.0',
    author="RealVNF",
    description="Interface definition between coordination algorithms and environments. "
                "Includes a dummy environment.",
    url='https://github.com/RealVNF/common-utils',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=requirements + test_requirements,
    tests_require=test_requirements,
    zip_safe=False,
)
