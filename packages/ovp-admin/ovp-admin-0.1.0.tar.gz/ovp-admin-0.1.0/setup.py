# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='ovp-admin',
    version='0.1.0',
    author=u'Atados',
    author_email='cid@atados.com.br, arroyo@atados.com.br',
    packages=['ovp_admin'],
    url='https://github.com/OpenVolunteeringPlatform/django-ovp-admin',
    download_url = 'https://github.com/OpenVolunteeringPlatform/django-ovp-admin/tarball/0.1.0',
    license='AGPL',
    description='This module includes admin functionality for' + \
                ' ovp modules.',
    long_description=open('README.rst', encoding='utf-8').read(),
    zip_safe=False,
    install_requires = [
      'Django>=1.10.1,<1.11.0',
    ]
)
