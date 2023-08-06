# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='django-transcrypt-exp',
    version='0.0.1-1',
    author=u'Morten B. Rasmussen',
    author_email='mbr@mr-systems.dk',
    packages=['django_transcrypt'],
    url='https://bitbucket.org/cruise/django_transcrypt',
    license='MIT, see LICENSE.txt',
    description='Adds livereload facility together with transcrypt python to' +
                ' javascript transpiling',
    long_description=open('README.txt').read(),
    zip_safe=False,
    install_requires=[
        'django-livereload-server',
        'Transcrypt'],
)
