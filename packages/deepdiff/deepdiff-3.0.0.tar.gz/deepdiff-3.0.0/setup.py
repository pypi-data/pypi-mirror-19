import os
from setuptools import setup

# if you are not using vagrant, just delete os.link directly,
# The hard link only saves a little disk space, so you should not care
if os.environ.get('USER', '') == 'vagrant':
    del os.link

try:
    with open('README.txt') as file:
        long_description = file.read()
except:
    long_description = "Deep Difference and Search of any Python object/data."

setup(name='deepdiff',
      version='3.0.0',
      description='Deep Difference and Search of any Python object/data.',
      url='https://github.com/seperman/deepdiff',
      download_url='https://github.com/seperman/deepdiff/tarball/master',
      author='Seperman',
      author_email='sep@zepworks.com',
      license='MIT',
      packages=['deepdiff'],
      zip_safe=False,
      test_suite="tests",
      tests_require=['mock'],
      long_description=long_description,
      # tests_require=['numpy==1.11.2'],  # Disabling this since Numpy does not install on pypy3
      classifiers=[
          "Intended Audience :: Developers",
          "Operating System :: OS Independent",
          "Topic :: Software Development",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: Implementation :: PyPy",
          "Development Status :: 5 - Production/Stable",
          "License :: OSI Approved :: MIT License"
      ],
      )
