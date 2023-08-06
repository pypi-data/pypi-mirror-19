#!/usr/bin/env python
import os
import sys
from setuptools import setup

try:
    import pandoc
except ImportError:
    pandoc = None

import jinja_app_loader as pkg


if sys.argv[-1] == 'publish':
    assert pandoc, 'You have to do: pip install pyandoc'
    os.system('python setup.py sdist upload')
    sys.exit(0)


def get_description():
    with open('README.md') as f:
        desc = f.read()
    short = desc.split('===\n')[1].strip().split('\n')[0]
    if pandoc:
        doc = pandoc.Document()
        doc.markdown = desc.encode('utf-8')
        desc = doc.rst.decode('utf-8')
    return short, desc


name = pkg.__name__
short, desc = get_description()
setup(
    version=pkg.__version__,
    name=name,
    url='https://github.com/imbolc/{}'.format(name),
    description=short,
    long_description=desc,

    py_modules=[name],
    install_requires=['jinja2'],

    author='Imbolc',
    author_email='imbolc@imbolc.name',
    license='ISC',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
