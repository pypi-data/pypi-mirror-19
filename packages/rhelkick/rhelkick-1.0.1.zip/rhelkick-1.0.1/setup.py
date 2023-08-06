from distutils.core import setup

setup(name='rhelkick',
      version='1.0.1',
      description='Generate and host a pxe server for RHEL-like distros.',
      author='Ryan Birmingham',
      author_email='birm@rbirm.us',
      url='http://rbirm.us',
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Information Technology'],
      long_description=open('README.md', 'r').read(),
      packages=['rhelkick'],
      )
