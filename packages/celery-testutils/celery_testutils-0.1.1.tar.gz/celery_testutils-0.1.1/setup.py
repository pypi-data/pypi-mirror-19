#!/usr/bin/env python
from setuptools import setup, find_packages

# convert the readme to pypi compatible rst
try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

setup(
    name='celery_testutils',
    version='0.1.1',
    author=u'Kevin Seelbach',
    author_email='kevin.seelbach@gmail.com',
    packages=find_packages(),
    url='http://github.com/kevinseelbach/celery_testutils',
    keywords=['celery','testing','integration','test'],
    license='BSD license, see LICENSE',
    description='Run a monitored Celery worker for integration tests that depend on Celery tasks',
    long_description=read_md('README.md'),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'celery>=3.0.19'
    ],
    test_suite='celery_testutils.tests'
)
