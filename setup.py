#!/usr/bin/env python
import glob
import os
from setuptools import setup, find_packages

base = os.path.dirname(os.path.abspath(__file__))

README_PATH = os.path.join(base, "README.rst")

install_requires = [
    'schematics>=2.0.0.dev2',
    'jinja2',
    'swagger-schema',
    'pyyaml',
]

tests_require = []

data_files = []

swagger_statics = glob.glob("transmute_core/swagger/static/**/")
for directory in swagger_statics:
    data_files.append(os.path.join("swagger", "static", directory, "*"))

setup(name='transmute-core',
      version='0.2.11',
      description=(
          "a utility library to help provide api route "
          "generation form function signature for web "
          "frameworks."
      ),
      long_description=open(README_PATH).read(),
      author='Yusuke Tsutsumi',
      author_email='yusuke@tsutsumi.io',
      url='https://github.com/toumorokoshi/transmute-core',
      # data_files=data_files,
      package_data={"transmute_core": data_files},
      packages=find_packages(),
      include_package_data=True,
      install_requires=install_requires,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Operating System :: MacOS',
          'Operating System :: POSIX :: Linux',
          'Topic :: System :: Software Distribution',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
      ],
      tests_require=tests_require
)
