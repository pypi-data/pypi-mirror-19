from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='mirbot',
      version='3.0.2',
      description='Modular Information Retrieval Bot (MIRbot)',
      long_description=readme(),
      url='https://github.com/pyratlabs/mirbot',
      author='PyratLabs',
      author_email='git@xan-manning.co.uk',
      license='MIT',
      packages=['mirbot'],
      scripts=['bin/mirbot'],
      install_requires=['python-daemon'],
      test_suite='nose.collector',
      tests_require=['nose'],
      classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
      ],
      zip_safe=False)
