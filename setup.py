# -*- coding: utf-8 -*-
"""
Setup for presence analyzer web app
"""
from setuptools import setup, find_packages
import os

NAME = "presence_analyzer"
VERSION = "0.1.0"


def read(*rnames):
    """
    Read data from file
    """
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(
    name=NAME,
    version=VERSION,
    description="Presence analyzer",
    long_description=read('README.md'),
    classifiers=[],
    keywords="",
    author="",
    author_email='',
    url='',
    license='MIT',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'Flask',
    ],
    entry_points="""
    [console_scripts]
    flask-ctl = presence_analyzer.script:run
    cron_jobs_update_xml = presence_analyzer.cron_jobs:update_users_xml

    [paste.app_factory]
    main = presence_analyzer.script:make_app
    debug = presence_analyzer.script:make_debug
    """,
)
