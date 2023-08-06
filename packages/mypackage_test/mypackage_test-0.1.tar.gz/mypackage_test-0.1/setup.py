from distutils.core import setup
setup(
  name = 'mypackage_test',
  packages = ['mypackage_test'], # this must be the same as the name above
  version = '0.1',
  description = 'A random test lib',
  author = 'Charles Darmon',
  author_email = 'charles.darmon@artefact.is',
  url = 'https://github.com/darmonc/hello-world', # use the URL to the github repo
  download_url = 'https://github.com/darmonc/hello-world/mypackage/0.1', # I'll explain this in a second
  keywords = ['testing', 'logging', 'example'], # arbitrary keywords
  classifiers = [],
)