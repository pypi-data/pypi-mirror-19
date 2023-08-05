#!/usr/bin/env
# -*- coding: utf-8 -*-
from setuptools  import setup
 
setup (
        name               = 'hanK_pki',
        version             = '0.0.4',
        py_modules      = ['hanK_pki'],
        author              = 'hanjungwook',
        author_email     = 'hjw0652@gmail.com',
        url                    = '',
        description        = 'Korea NPKI Auth Module',
	install_requires = [
		'Crypto',
		'pyasn1',
		'cryptography',
		'passlib',
		],
    )
