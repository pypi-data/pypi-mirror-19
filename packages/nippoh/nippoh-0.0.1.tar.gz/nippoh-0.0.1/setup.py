# -*- coding:utf-8 -*-
import os
from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))


setup(
    name='nippoh',
    author='imagawa_yakata(oyakata)',
    author_email='imagawa.hougikumaru@gmail.com',
    version='0.0.1',
    url='https://bitbucket.org/imagawa_yakata/nippoh',
    licence='MIT',
    description='日報',
    entry_points={'console_scrpts': ['nippho=nippoh.main']},
    py_modules=['nippoh'],
)
