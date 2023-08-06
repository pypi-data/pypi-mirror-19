from distutils.core import setup

setup(name='dbops',
      version='2.0.0',
      description='Database Operations Tools',
      author='Ryan Birmingham',
      author_email='birm@rbirm.us',
      url='http://rbirm.us',
      classifiers=['Development Status :: 4 - Beta', 'Topic :: Database',
                   'Intended Audience :: Information Technology'],
      long_description=open('readme.md', 'r').read(),
      packages=['dbops'],
      )
