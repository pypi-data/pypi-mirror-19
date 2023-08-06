# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

setup(
    name='easyRedisCache',
    version='0.11',
    author=u'David Ziegler',
    author_email='webmaster@SpreadPost.de',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/InfinityMod/easyRedisCache',
    license='BSD',
    description='Easy lock secured cache for redis',
    zip_safe=False,
    keywords=['cache', 'lock', 'memcached', 'redis'],
    install_requires=[
        'sherlock',
        'redis'
    ],
)