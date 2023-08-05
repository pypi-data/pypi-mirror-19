# coding: utf-8

import os
from setuptools import setup, find_packages


def version():
    bd = os.path.dirname(__file__)

    with open(os.path.join(bd, 'pyicao9303/version.py')) as f:
        l = dict()
        exec(f.read(), l)

        return l['VERSION']

setup(
    name='pyicao9303',
    version=version(),
    author='Konstantin Kruglov',
    author_email='kruglovk@gmail.com',
    description='empty',
    url='https://github.com/k0st1an/pyicao9303/',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'icao9303 = pyicao9303:cli',
        ],
    },
    install_requires=[
        'click==6.6',
    ],
    license='Apache License Version 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: POSIX :: Linux',
    ],
)
