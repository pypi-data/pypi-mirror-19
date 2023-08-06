# -*- coding: utf-8 -*-

import setuptools
from distutils.core import setup
import io
import re
import os


DOC = '''
## 一、安装

> **pip install auto-provider**

然后在系统中会得到一个 `auto-provider` 的命令 cli 工具。


## 二、使用

简单使用方法如下：

> **auto-provider -p platform**

或者使用 `auto-provider --help` 查看帮助信息和具体详细的使用方法。

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


setup(name='auto-provider',
      version=find_version('provider/__init__.py'),
      description=('device provider for automation test.'),
      long_description=DOC,
      author='hustcc',
      author_email='i@hust.cc',
      url='https://github.com/hustcc',
      license='GPL',
      install_requires=[
        'click',
        'zmq'
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
        'Topic :: Utilities'
      ],
      keywords='device, provider',
      include_package_data=True,
      zip_safe=False,
      packages=['provider'],
      entry_points={
        'console_scripts': ['auto-provider=provider.cli:run']
      })
