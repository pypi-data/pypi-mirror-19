#!/usr/bin/env python

from setuptools import setup, find_packages

# to set __version__
exec(open('blockstack_client/version.py').read())

setup(
    name='blockstack-client',
    version=__version__,
    url='https://github.com/blockstack/blockstack-client',
    license='GPLv3',
    author='Blockstack.org',
    author_email='support@blockstack.org',
    description='Python client library for Blockstack',
    keywords='blockchain bitcoin btc cryptocurrency name key value store data',
    packages=find_packages(),
    scripts=['bin/blockstack'],
    download_url='https://github.com/blockstack/blockstack-cli/archive/master.zip',
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'virtualchain>=0.14.0',
        'protocoin>=0.2',
        'blockstack-profiles>=0.14.0',
        'pybitcoin>=0.9.9',
        'blockstack-zones>=0.14.0',
        'defusedxml>=0.4.1',
        'keylib>=0.0.5',
        'mixpanel>=4.3.1',
        'pycrypto>=2.6.1',
        'simplejson>=3.8.2',
        'jsonschema>=2.5.1',
        'basicrpc>=0.0.2',      # DHT storage driver
        'boto>=2.38.0'          # S3 storage driver
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2 :: Only',
        'Topic :: Internet',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
