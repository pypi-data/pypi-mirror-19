import os
import sys

from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

required = [
    'requests>=0.10.0',
    'hashlib',
    'tqdm',
    'six'
]

setup(
  name='voyage',
  version='0.1.2',
  packages=['voyage'],
  url='http://voyage.ai',
  license='',
  install_requires=required,
  author='Eric Gonzalez',
  author_email='eric@voyage.ai',
  description='Python Client'
)
