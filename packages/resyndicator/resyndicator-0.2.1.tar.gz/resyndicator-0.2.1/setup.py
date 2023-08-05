#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='resyndicator',
    version='0.2.1',
    author='Denis Drescher',
    author_email='denis.drescher+resyndicator@claviger.net',
    url='https://bitbucket.org/Telofy/resyndicator',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'utilofies',
        'twython',
        'requests',
        'python-dateutil',
        'feedparser',
        'SQLAlchemy',
        'awesome-slugify',
        'beautifulsoup4',
        'psycopg2',
        'readability-lxml',
        'xmltodict',
        'cached-property',
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'resyndicator = resyndicator.console:run'
        ]
    }
)
