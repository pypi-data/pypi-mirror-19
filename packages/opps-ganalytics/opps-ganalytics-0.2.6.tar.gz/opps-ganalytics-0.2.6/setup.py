#!/usr/bin/env python
# -*- coding:utf-8 -*-
from setuptools import setup, find_packages


VERSION = (0, 2, 6)

__version__ = ".".join(map(str, VERSION))
__status__ = "Development"
__description__ = u"Google Analytics for Opps CMS"
__author__ = u"Thiago Avelino"
__credits__ = ['Jean Rodrigues']
__email__ = u"thiagoavelinoster@gmail.com"
__copyright__ = u"Copyright 2015, YACOWS"

install_requires = ["opps", "django-celery", "google-api-python-client"]

classifiers = ["Development Status :: 4 - Beta",
               "Intended Audience :: Developers",
               "Operating System :: OS Independent",
               "Framework :: Django",
               'Programming Language :: Python',
               "Programming Language :: Python :: 2.7",
               "Operating System :: OS Independent",
               "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
               'Topic :: Software Development :: Libraries :: Python Modules']

try:
    long_description = open('README.md').read()
except:
    long_description = __description__

setup(
    name='opps-ganalytics',
    namespace_packages=['opps'],
    version=__version__,
    description=__description__,
    long_description=long_description,
    classifiers=classifiers,
    keywords='google analytics top read',
    author=__author__,
    author_email=__email__,
    packages=find_packages(exclude=('doc', 'docs',)),
    install_requires=install_requires,
    package_dir={'opps': 'opps'},
    include_package_data=True
)
