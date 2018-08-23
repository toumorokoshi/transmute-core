#!/usr/bin/env python
import glob
import os
import sys
from setuptools import setup, find_packages

is_release = False
if "--release" in sys.argv:
    is_release = True
    sys.argv.remove("--release")

base = os.path.dirname(os.path.abspath(__file__))

README_PATH = os.path.join(base, "README.rst")

install_requires = [
    'attrs>=17.3.0',
    'cattrs>=0.5.0, <=0.6.0',
    'jsonschema-extractor>=0.6.0',
    'schematics>=2.0.0',
    'six',
    'swagger-schema>=0.5.1',
    'pyyaml',
]

if sys.version_info < (3, 5):
    install_requires.append("typing")

if sys.version_info < (3, 4):
    install_requires.append("singledispatch")

tests_require = []

data_files = []

swagger_statics = glob.glob("transmute_core/swagger/static/**/")
for directory in swagger_statics:
    data_files.append(os.path.join("swagger", "static", directory, "*"))

setup(name='transmute-core',
      setup_requires=["vcver"],
      vcver={
          "is_release": is_release,
          "path": base
      },
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
