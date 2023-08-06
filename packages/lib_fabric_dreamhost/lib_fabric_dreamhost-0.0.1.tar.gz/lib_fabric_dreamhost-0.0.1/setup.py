# -*- coding:utf-8 -*-
from setuptools import setup

setup(name='lib_fabric_dreamhost',
      version='0.0.1',
      description='Lib with shared Fabric tasks to be used with Dreamhost.',
      url='https://bitbucket.org/fernandoe/lib-fabric-dreamhost',
      author='Fernando Espíndola',
      author_email='fer.esp@gmail.com',
      license='MIT',
      packages=['lib_fabric_dreamhost'],
      install_requires=[
          'Fabric==1.13.1',
          'Jinja2==2.9.4'
      ],
      zip_safe=False,
      include_package_data=True)
