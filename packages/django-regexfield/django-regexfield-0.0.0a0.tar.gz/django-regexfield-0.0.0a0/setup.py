from distutils.core import setup

from setuptools import find_packages

import regexfield

try:
    with open('README.rst') as readme:
        long_description = readme.read()
except:
    long_description = ''

setup(
    name='django-regexfield',
    version=regexfield.__version__,
    packages=find_packages(),
    url='https://github.com/vinayinvicible/django-regexfield',
    license='MIT',
    author='Vinay Karanam',
    author_email='vinayinvicible@gmail.com',
    description='RegexField for Django models',
    long_description=long_description,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],
    zip_safe=False,
)
