#!/usr/bin/env python
# coding=UTF-8
from setuptools import setup

setup(name='CoolAMQP',
      version='0.7',
      description=u'AMQP client with sane reconnects',
      author=u'DMS Serwis s.c.',
      author_email='piotrm@smok.co',
      url='https://github.com/smok-serwis/coolamqp',
      download_url='https://github.com/smok-serwis/coolamqp/archive/master.zip',
      keywords=['amqp', 'pyamqp', 'rabbitmq', 'client', 'network', 'ha', 'high availability'],
      packages=['coolamqp', 'coolamqp.backends'],
      license='MIT License',
      long_description=u'The AMQP client that handles reconnection madness for you',
      requires=[
            "amqp",
            "six",
            "monotonic"
      ],
      tests_require=["nose"],
      test_suite='nose.collector',
      classifiers=[
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
#            'Programming Language :: Python :: 3.4',
#            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: Implementation :: PyPy',
            'Operating System :: OS Independent'
      ]
     )
