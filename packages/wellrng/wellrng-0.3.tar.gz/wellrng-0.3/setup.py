from setuptools import setup

setup(
  name = 'wellrng',
  packages = ['wellrng'],
  version = '0.3',
  description = 'A replacment for the default random lib using WELL1024a RNG',
  author = 'Raphael Stefanini',
  author_email = 'rphl@rphl.net',
  url = 'https://github.com/rphlo/py-wellrng',
  download_url = 'https://github.com/rphlo/py-wellrng/tarball/0.3',
  keywords = ['random', 'well1024a', 'PRNG', 'RNG'],
  classifiers = [
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
  ],
)
