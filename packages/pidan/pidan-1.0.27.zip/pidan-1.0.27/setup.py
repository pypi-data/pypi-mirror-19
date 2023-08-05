# install:python setup.py sdist upload
# -*- coding:utf-8 -*-
from distutils.core import setup
 
setup (
    name = 'pidan',
    version = '1.0.27',
    packages=["pidan"],
    platforms=['any'],
    author = 'chengang',
    author_email = 'chengang.net@gmail.com',
    description = u'临时版本',
    package_data = {
        '': ['*.data'],
    },
)