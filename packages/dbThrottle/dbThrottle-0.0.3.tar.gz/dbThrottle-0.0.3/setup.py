from distutils.core import setup

setup(name='dbThrottle',
      version='0.0.3',
      description='Python Class to run code with consideration to DB load.',
      author='Ryan Birmingham',
      author_email='birm@rbirm.us',
      url='http://rbirm.us',
      classifiers=['Development Status :: 1 - Planning',
                   'Programming Language :: Python :: 3.3',
                   'Topic :: Database',
                   'Intended Audience :: Information Technology',
                   'Programming Language :: SQL',
                   'Programming Language :: PL/SQL',
                   'Programming Language :: Python :: 2.7',
                   'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
      long_description=open('readme.md', 'r').read(),
      packages=['dbThrottle'],
      )
