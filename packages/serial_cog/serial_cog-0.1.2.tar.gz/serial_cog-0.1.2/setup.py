import os

import yaml
from setuptools import setup
from setuptools.command.install import install

setup(
    name='serial_cog',
    version='0.1.2',
    packages=['serial_cog.modules'],
    url='https://github.com/Rashitko/serial_provider_cog',
    download_url='https://github.com/Rashitko/serial_provider_cog/master/tarball/0.1',
    license='MIT',
    author='Michal Raska',
    author_email='michal.raska@gmail.com',
    description='',
    install_requires=['up', 'pyyaml', 'pyserial'],
)
