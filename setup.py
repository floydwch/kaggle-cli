#!/usr/bin/env python
from setuptools import setup, find_packages

from kaggle_cli.meta import VERSION


PROJECT = 'kaggle-cli'


long_description = \
    'https://github.com/floydsoft/kaggle-cli/blob/master/README.md'

setup(
    name=PROJECT,
    version=VERSION,

    description='An unofficial Kaggle command line tool.',
    long_description=long_description,

    author='floydsoft',
    author_email='floydsoft@gmail.com',

    url='https://github.com/floydsoft/kaggle-cli',
    download_url='https://github.com/floydsoft/kaggle-cli/tarball/master',

    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.4',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],

    platforms=['Any'],

    scripts=[],

    provides=[],
    install_requires=['cliff', 'MechanicalSoup', 'lxml', 'cssselect', 'configparser'],

    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'kg = kaggle_cli.main:main'
        ],
        'kaggle_cli': [
            'submit = kaggle_cli.submit:Submit',
            'config = kaggle_cli.config:Config',
            'download = kaggle_cli.download:Download',
            'dataset = kaggle_cli.download:Dataset'
        ],
    },

    zip_safe=False,
)
