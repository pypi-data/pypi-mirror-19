import os

import yaml
from setuptools import setup
from setuptools.command.install import install

setup(
    name='mission_control_cog',
    version='0.1',
    packages=['mission_control_cog', 'mission_control_cog.modules'],
    url='https://github.com/Rashitko/mission-control-cog',
    download_url='https://github.com/Rashitko/mission-control-cog/master/tarball/',
    license='MIT',
    author='Michal Raska',
    author_email='michal.raska@gmail.com',
    description='',

    install_requires=['up', 'twisted', 'pyyaml'],
)
