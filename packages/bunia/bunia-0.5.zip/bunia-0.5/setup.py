#!/usr/bin/env python
#coding=UTF-8
from distutils.core import setup

setup(name='bunia',
      version='0.5',
      description=u'Write commands that use multiple interfaes',
      author=u'Piotr Maślanka',
      author_email='piotrm@smok.co',
      url='https://github.com/smok-serwis/bunia',
      download_url='https://github.com/smok-serwis/bunia/archive/master.zip',
      keywords=['arguments', 'argparse', 'html', 'console'],
      platforms=['any'],
      packages=['bunia',
                'bunia.runner',
                'bunia.api',
                'bunia.output',
                ],
      license='MIT License',
      long_description=u'''This is an interface for writing commands that can use multiple interfaces, ie. you can launch
it from shell, Web, SMS, etc.

A device-independent output and input is presented.''',
      classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Operating System :: OS Independent'
      ]
)