#!/usr/bin/env python
# coding: utf8

import sys

from setuptools import setup

sys.path.insert(0, 'mdeditor')
sys.path.pop(0)

with open('README.rst') as f:
    README = f.read()

setup(
    name='mdeditor',
    version='0.3.1',
    description='markdown editor web',
    long_description=README,
    author='kghch',
    author_email='wanghan0307@gmail.com',
    url='https://github.com/kghch/md_editor',
    packages=['mdeditor', 'mdeditor.templates', 'mdeditor.static', 'mdeditor.static.lib',
		'mdeditor.static.lib.css', 'mdeditor.static.lib.fonts', 'mdeditor.static.lib.js',
		'mdeditor.static.lib.css.themes.default.assets.fonts'
	],
    include_package_data=True,
    package_data={
        'mdeditor.templates': ['*.html'],
        'mdeditor.static': ['*.css', '*.js'],
	'mdeditor.static.lib': ['*.*'],
	'mdeditor.static.lib.css': ['*.css'],
	'mdeditor.static.lib.fonts': ['*.*'],
	'mdeditor.static.lib.js': ['*.js'],
	'mdeditor.static.lib.css.themes.default.assets.fonts': ['*.*']},
    install_requires=['tornado', 'torndb', 'MySQL-python', 'markdown', 'evernote'],
    entry_points={
        'console_scripts': [
            'mdeditor = mdeditor:main',
        ],
    }
)
