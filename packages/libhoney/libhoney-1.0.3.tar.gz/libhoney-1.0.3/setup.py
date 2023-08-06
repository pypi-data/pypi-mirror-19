import subprocess
import sys
from setuptools import setup
sys.path.append('libhoney/')

from version import VERSION


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'publish':
            subprocess.check_call('git push --follow-tags && python setup.py sdist upload',
                                  shell=True)
            return
    setup(name='libhoney',
          version=VERSION,
          description='Python library for sending data to Honeycomb',
          url='https://github.com/honeycombio/libhoney-py',
          author='Honeycomb.io',
          author_email='feedback@honeycomb.io',
          license='Apache',
          packages=['libhoney'],
          install_requires=[
              'requests',
              'transmission',
              'statsd',
              'six',
          ],
          zip_safe=False)

if __name__ == '__main__':
    main()
