from setuptools import setup, find_packages
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mcg',

    version='0.0.6',

    description='Meteor Project and API generator',
    long_description=long_description,

    url='https://github.com/BizarroSolutions/mcg',

    author='Bizarro Solutions (João Marcos Bizarro)',
    author_email='info@bizarro.solutions',

    license='GNU General Public License v3 (GPLv3)',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

         'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='mcg productivity meteor development',

    packages=find_packages(),

    install_requires=['cement', 'pymongo', 'faker'],

    entry_points={
        'console_scripts': [
            'mcg=mcg:main',
        ],
    },
)
