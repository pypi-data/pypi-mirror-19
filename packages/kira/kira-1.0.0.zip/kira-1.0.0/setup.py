"""Setup for Kira."""

from setuptools import setup, find_packages
# Encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get long description
with open(path.join(here, 'README.rst'), encoding='utf-8') as description_file:
    long_description = description_file.read()

# Setup
setup(
    name='kira',

    version='1.0.0',

    description='A Python MAL API',
    long_description=long_description,

    url='https://github.com/datlofdev/Kira',

    author='Jackson Ca. Rakena',
    author_email='jackson.rakena2@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development:: Utilities',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.5',
    ],

    keywords='development myanimelist mal',

    py_modules=["kira"],

    install_requires=['requests'],

    entry_points={
        'console_scripts': [
            'kira=kira:main',
        ],
    },
)