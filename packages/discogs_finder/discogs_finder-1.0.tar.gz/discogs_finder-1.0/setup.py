from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

def requirements():
    with open('requirements.txt') as f:
        return f.read()

setup(name='discogs_finder',
      version='1.0',
      description='FIND Every Release in your collection',
      long_description=readme(),
      url='https://github.com/tim6her/discogs_finder',
      author='Tim B. Herbstrith',
      license='MIT',
      packages=['discogs_finder'],
      install_requires=requirements(),
      scripts=['scripts/discogs-finder'],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
