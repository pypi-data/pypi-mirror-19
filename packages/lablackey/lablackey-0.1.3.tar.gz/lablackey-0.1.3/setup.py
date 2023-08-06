from setuptools import setup

setup(
  name = 'lablackey',
  packages = ['lablackey','lablackey.db'],
  version = '0.1.3',
  description = 'A collection of tools for django',
  author = 'Chris Cauley',
  author_email = 'chris@lablackey.com',
  url = 'https://github.com/chriscauley/lablackey',
  keywords = ['utils','django'],
  license = 'GPL',
  include_package_data = True,
)
