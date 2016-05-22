# Always prefer setuptools over distutils
from setuptools import setup
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django_bootstrap3_daterangepicker',
    version='1.0.0b3',

    description='Django date range form field',
    long_description=long_description,

    url='https://github.com/YuriMalinov/django-bootstrap3-daterangepicker/',

    author='Yuri Malinov',
    author_email='yurik.m@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='django daterange picker',
    packages=['django_bootstrap3_daterangepicker'],
    install_requires=['django'],
    include_package_data=True,
)
