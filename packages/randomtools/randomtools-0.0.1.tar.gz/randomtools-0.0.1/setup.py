import sys

from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


def version():
    with open('randomtools/__init__.py') as f:
        for line in f:
            if line.startswith('__version__'):
                return line.split(r"'")[1]

needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []


setup(name='randomtools',
      version=version(),
      description='Creating (unsecure) sequences and generators of random numbers.',
      long_description=readme(),
      keywords='random utility',
      platforms=["Windows Linux Mac OS-X"],

      classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Utilities',
      ],

      url='https://github.com/MSeifert04/randomtools',
      author='Michael Seifert',
      author_email='michaelseifert04@yahoo.de',

      install_requires=[
          ],

      setup_requires=[
          ] + pytest_runner,

      tests_require=[
          'pytest',
          ],

      license='Apache License Version 2.0',
      packages=['randomtools'],
      zip_safe=False)
