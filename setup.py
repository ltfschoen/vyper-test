# -*- coding: utf-8 -*-
# Reference: https://docs.pytest.org/en/latest/goodpractices.html#test-discovery

from setuptools import setup, find_packages

setup(
    name='vyper',
    version='0.0.4',
    description='Vyper Programming Language for Ethereum',
    author='Vitalik Buterin',
    url='https://github.com/ethereum/vyper',
    packages=find_packages(exclude=('tests')),
    install_requires=['py-evm>=0.2.0a12'],
    setup_requires=['pytest-runner'],
    python_requires='>=3.6',
    tests_require=['pytest', 'pytest-cov', 'ethereum==2.3.1'],
    scripts=['bin/vyper', 'bin/vyper-serve', 'bin/vyper-run']
)