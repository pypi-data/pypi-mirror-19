'''Importing setuptools and configuring setup attributes'''
from setuptools import setup

setup(name='buzzfizz',
      version='0.2',
      description='Sample BuzzFuzz program used for screening',
      url='https://github.com/m1kelyons/buzzfizz',
      author='Mike Lyons',
      license='MIT',
      packages=['buzzfizz'],
      zip_safe=False)
