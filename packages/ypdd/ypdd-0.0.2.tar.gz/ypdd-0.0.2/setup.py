# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


def version():
    bd = os.path.dirname(__file__)

    with open(os.path.join(bd, 'ypdd/version.py')) as f:
        l = dict()
        exec(f.read(), l)

        return l['VERSION']

setup(
    name='ypdd',
    version=version(),
    author='Konstantin Kruglov',
    author_email='kruglovk@gmail.com',
    description='library for YandexPDD',
    url='https://github.com/k0st1an/yandex-pdd',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'yandex-pdd = ypdd.cli:cli',
        ],
    },
    install_requires=[
        'click==6.6',
        'requests==2.12.4',
    ],
    license='Apache License Version 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: POSIX :: Linux',
    ],
)
