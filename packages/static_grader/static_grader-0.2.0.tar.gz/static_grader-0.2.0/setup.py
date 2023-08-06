from setuptools import setup
from static_grader import __version__

setup(name='static_grader',
  version=__version__,
  description='A Static grader',
  author='The Data Incubator',
  packages=['static_grader'],
  install_requires=[
    'requests'
  ]
)
