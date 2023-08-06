#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='aws-is-instance-healthy',
    version='0.4.3',
    packages=find_packages(),
    license='MIT',
    author='Marcos Araujo Sobrinho',
    author_email='marcos.sobrinho@vivareal.com',
    url='http://www.vivareal.com.br/',
    scripts=['vivareal/cli/am_i_healthy.py', 'vivareal/cli/is_instance_healthy.py'],
    long_description=open('README.rst').read(),
    install_requires=open('requirements.txt').read().strip('\n').split('\n')
)
