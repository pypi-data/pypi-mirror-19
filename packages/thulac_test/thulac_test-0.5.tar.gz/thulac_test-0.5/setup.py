# from distutils.core import setup, find_packages
from setuptools import setup, find_packages
from distutils.core import Extension
my_c_exten = Extension('asdf', sources=[''])

setup(
  name = 'thulac_test',
  # packages = ['thulac_test'], # this must be the same as the name above
  version = '0.5',
  description = 'A random test lib',
  author = 'Peter Downs',
  author_email = 'majunhua133256@gmail.com',
  url = 'https://github.com/thunlp/THULAC-Python', # use the URL to the github repo
  download_url = 'https://github.com/thunlp/THULAC-Python/archive/master.zip', # I'll explain this in a second
  keywords = ['testing', 'logging', 'example'], # arbitrary keywords
  classifiers = [],
  packages = find_packages(),
  ext_modules=[my_c_exten],
)