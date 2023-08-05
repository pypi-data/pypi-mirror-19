from distutils.core import setup
setup(
  name = 'django-buildout-sample-mfx',
  packages = ['django-buildout-sample-mfx'], # this must be the same as the name above
  version = '0.1',
  description = 'A random test lib',
  author = 'Michał Frąckkowiak',
  author_email = 'mfxovh@gmail.com',
  url = 'https://github.com/mfxpl/django-buildout-sample', # use the URL to the github repo
  download_url ='https://github.com/mfxpl/django-buildout-sample/tarball/0.1', # I'll explain this in a second
  keywords = ['testing', 'logging', 'example'], # arbitrary keywords
  classifiers = [],
)


# from setuptools import setup, find_packages
#
# setup(
#     name = "django-shorturls",
#     version = "1.0",
#     url = 'https://github.com/mfxpl/django-buildout-sample.git',
#     license = 'GNU',
#     description = "A short URL handler for Django apps.",
#     author = 'Michał Frąckowiak',
#     packages = find_packages('src'),
#     package_dir = {'': 'src'},
#     install_requires = ['setuptools'],
# )