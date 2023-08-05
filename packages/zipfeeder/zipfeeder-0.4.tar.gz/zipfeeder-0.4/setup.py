from distutils.core import setup
setup(
  name='zipfeeder',
  packages = ['zipfeeder'],
  version = '0.4',
  description = 'Uses the Zipfeeder.us API to serve free United States Zip Code information, a ZipFeeder account '
                'is required',
  author = 'Paul Thompson',
  author_email = 'info@zipfeeder.us',
  install_requires=[
          'requests',
  ],
  url = 'https://github.com/rpupkin77/zipfeeder.py',
  download_url = 'https://github.com/rpupkin77/zipfeeder.py/archive/master.zip',
  keywords = ['zip code', 'us zip code', 'postal code', 'zip code api'],
  classifiers = [],
)