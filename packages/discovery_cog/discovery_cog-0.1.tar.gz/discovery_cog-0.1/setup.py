import os

import yaml
from setuptools import setup
from setuptools.command.install import install

setup(
    name='discovery_cog',
    version='0.1',
    packages=['discovery_cog', 'discovery_cog.modules'],
    url='https://github.com/Rashitko/discovery_cog',
    download_url='https://github.com/Rashitko/discovery_cog/master/tarball/',
    license='MIT',
    author='Michal Raska',
    author_email='michal.raska@gmail.com',
    description='',
    install_requires=['up', 'twisted', 'pyyaml'],
)
