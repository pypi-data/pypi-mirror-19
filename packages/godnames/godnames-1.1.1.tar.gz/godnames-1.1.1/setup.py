from setuptools import setup

setup(
  name = 'godnames',
  packages = ['godnames'],
  version = '1.1.1',
  description = 'A library to generate randomly names',
  author = 'Raphael Stefanini',
  author_email = 'rphl@rphl.net',
  url = 'https://github.com/rphlo/py-godnames',
  download_url = 'https://github.com/rphlo/py-godnames/tarball/1.1.1',
  keywords = ['random', 'naming', 'name'],
  classifiers = [
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
  ],
  entry_points = {
    'console_scripts': ['godname=godnames.command_line:main'],
  }
)
