# -*- coding: utf-8 -*-
import setuptools  # noqa
from distutils.core import setup
import io
import re
import os


DOC = '''
## 1. Install

> **pip install http-here**

Then get a cli command named `http-here`.


## 2. Usage

CLI command **http-here**，How to use it：

> **http-here [port]**

Or `hint --help` to get documents.

```shell
$ http-here --help
Usage: http-here [OPTIONS] [PORT]

Options:
  --host TEXT  The binding host of server.
  --help       Show this message and exit.
```
'''


def read(*names, **kwargs):
    return io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ).read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(name='http-here',
      version=find_version('run.py'),
      description=('Simple Python HTTP server short for SimpleHTTPServer.'),
      long_description=DOC,
      author='hustcc',
      author_email='i@hust.cc',
      url='https://github.com/hustcc',
      license='MIT',
      install_requires=[
        'click'
      ],
      classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities'
      ],
      keywords='server, http, httpserver, simple, SimpleHTTPServer',
      py_modules=['run'],
      entry_points={
        'console_scripts': ['http-here=run:run']
      })
