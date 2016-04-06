#!/usr/bin/env python
import glob
import os
from setuptools import setup, find_packages

base = os.path.dirname(os.path.abspath(__file__))

README_PATH = os.path.join(base, "README.rst")

install_requires = [
    'schematics',
    'jinja2',
    'swagger-schema',
    'pyyaml',
]

tests_require = []

data_files = [
    ("web_transmute/swagger", ["web_transmute/swagger/swagger.html"])
]

directories = glob.glob("web_transmute/swagger/static/**/")
for directory in directories:
    files = [
        f for f in glob.glob(directory+'*') if not os.path.isdir(f)
    ]
    data_files.append((directory, files))

setup(name='web-transmute',
      version='0.0.7b',
      description=(
          "a utility library to help provide api route "
          "generation form function signature for web "
          "frameworks."
      ),
      long_description=open(README_PATH).read(),
      author='Yusuke Tsutsumi',
      author_email='yusuke@tsutsumi.io',
      url='',
      data_files=data_files,
      packages=find_packages(),
      install_requires=install_requires,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Operating System :: MacOS',
          'Operating System :: POSIX :: Linux',
          'Topic :: System :: Software Distribution',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
      ],
      tests_require=tests_require
)
