# http://stackoverflow.com/questions/9810603/adding-install-requires-to-setup-py-when-making-a-python-package
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
  name = 'dekoruma_indexer',
  version = '0.1.1',
  description = 'A package for indexer algolia',
  author = 'Dekoruma',
  author_email = 'hello@dekoruma.com',
  url = 'https://github.com/jekidekoruma/indexer', # use the URL to the github repo
  py_modules=['dekoruma_indexer.base_indexer'],
  install_requires=[
    'algoliasearch>=1.11,<1.12',
    'Django>=1.9,<1.10',
    'django-rq>=0.9,<0.10'
  ]
)