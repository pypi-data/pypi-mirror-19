from setuptools import setup
setup(
  name = 'pyiss',
  packages = ['pyiss'], # this must be the same as the name above
  install_requires = ['requests', 'httmock', 'voluptuous'],
  version = '1.0.1',
  description = 'A simple python3 library for info about the current '
                'International Space Station location',
  author = 'Hydreliox',
  author_email = 'hydreliox@gmail.com',
  license = 'MIT',
  url = 'https://github.com/HydrelioxGitHub/pyiss', # use the URL to the
  # github repo
  download_url = 'https://github.com/HydrelioxGitHub/pyiss/tarball/1.0.1',
  keywords = ['ISS', 'space', 'station', 'API'], # arbitrary keywords
  classifiers = [],
  test_suite='nose.collector',
  tests_require=['nose'],
)
