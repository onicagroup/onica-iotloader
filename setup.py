"""Packaging settings."""

from codecs import open as codecs_open
from os.path import abspath, dirname, join

from setuptools import setup, find_packages
from onica_iotloader import __version__

THIS_DIR = abspath(dirname(__file__))
with codecs_open(join(THIS_DIR, 'README.md'), encoding='utf-8') as readfile:
    LONG_DESCRIPTION = readfile.read()

setup(
    name='onica_iotloader',

    version=__version__,

    description='A tool to load bulk simulation data into AWS IoT Analytics',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",

    # The project's main homepage.
    url='https://github.com/onicagroup/onica-iotloader',

    # Author details
    author='Onica Group LLC',
    author_email='opensource@onica.com',

    # Choose your license
    license='Apache License 2.0',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],

    keywords='iot cli',

    packages=find_packages(exclude=['docs', 'tests*']),

    install_requires=['boto3', 'docopt'],

    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

    entry_points={
        'console_scripts': [
            'onica-iotloader=onica_iotloader.cli:main',
        ],
    }
)
