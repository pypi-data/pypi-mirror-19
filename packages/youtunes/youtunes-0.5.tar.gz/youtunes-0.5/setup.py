from setuptools import setup
setup(
  name = 'youtunes',
  packages = ['main'],
  version = '0.5',
  description = 'Multithreaded direct download from youtube to mp3',
  author = 'Andrew Chang',
  author_email = 'achang97@stanford.edu',
  license = 'MIT',
  url = 'https://github.com/achang97/YouTunes',
  download_url = 'https://github.com/achang97/youtunes/tarball/0.5',
  keywords = ['download', 'YouTube', 'iTunes'],
  classifiers = [
    'Operating System :: MacOS',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7'
  ],
  py_modules=['main.py'],
  scripts=['youtunes'],
  install_requires = [
        'urllib',
        'urllib2',
        'youtube_dl',
        'HTMLParser',
        'bs4',
        'eyed3',
        'requests',
        'ffprobe',
        'avprobe'
  ]
)
