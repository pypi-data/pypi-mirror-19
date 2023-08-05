#!/usr/bin/env python
import os
from setuptools import setup, find_packages

# convert the readme to pypi compatible rst
try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

def get_version(package):
    v = {}
    with open(os.path.join(os.path.split(__file__)[0], package, '__version__.py'), "r") as init_file:
        for line in init_file.readlines():
            if line.startswith("__version__ = "):
                _, val = line.split("=")
                val = eval(val.strip())
                return val


setup(
    name='celery_testutils',
    version=get_version('celery_testutils'),
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
