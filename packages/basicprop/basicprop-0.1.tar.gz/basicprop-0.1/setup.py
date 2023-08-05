from distutils.core import setup

setup(
  name = 'basicprop',
  packages = ['basicprop'], # this must be the same as the name above
  version = '0.1',
  description = 'A synthetic dataset used for generative models',
  author = 'Andrew Drozdov',
  author_email = 'andrew@mrdrozdov.com',
  url = 'https://github.com/mrdrozdov/basicprop', # use the URL to the github repo
  download_url = 'https://github.com/mrdrozdov/basicprop/tarball/0.1', # I'll explain this in a second
  keywords = ['deep-learning', 'gan', 'dataset'], # arbitrary keywords
  classifiers = [],
)
