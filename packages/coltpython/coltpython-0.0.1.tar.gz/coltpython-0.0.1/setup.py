"""
A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='coltpython',

    description='A framework and manager for native services.',
    long_description=long_description,

    version='0.0.1',
    keywords='coltpython service os',

    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    url='https://github.com/AdrianGhita/coltpython',
    download_url='https://github.com/AdrianGhita/coltpython.git',

    author='Adrian Ghiță',
    author_email='adi.ghita202@gmail.com',
    maintainer='Adrian Ghiță',
    maintainer_email='adi.ghita202@gmail.com',

    license='MIT',

    install_requires=[],
    extras_require={
        'dev': ['pytest', 'sphinx'],
    },

    packages=find_packages('src'),
    package_dir={
        '': 'src'
    },

    package_data={
    },

    entry_points={
        'console_scripts': [
        ],
    },
)
