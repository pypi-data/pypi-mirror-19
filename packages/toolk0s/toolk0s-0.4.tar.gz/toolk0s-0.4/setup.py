from setuptools import setup

try:
    description = file('README.txt').read()
except IOError:
    description = ''

version = "0.4"

# dependencies
dependencies = [
    'WebOb',
    'tempita',
    'paste',
    'pastescript', # technically optional, but here for ease of install
    'whoosh >= 2.5',
    'couchdb',
    'docutils',
    'pyloader',
    'theslasher',
    'pyes == 0.15',
    ]

setup(name='toolk0s',
      version=version,
      description="a place to list links + tools",
      long_description=description,
      classifiers=[], # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      author='Jeff Hammel',
      author_email='jhammel@mozilla.com',
      url='http://k0s.org/hg/toolbox/',
      license="MPL",
      packages=['toolbox'],
      include_package_data=True,
      zip_safe=False,
      install_requires=dependencies,
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      toolbox-convert-model = toolbox.model:convert
      toolbox-serve = toolbox.factory:main

      [paste.app_factory]
      toolbox = toolbox.factory:paste_factory
      """,
      )
