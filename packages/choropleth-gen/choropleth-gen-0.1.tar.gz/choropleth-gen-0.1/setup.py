#!/usr/bin/python3
# coding=utf8

from setuptools import setup, find_packages

setup(
    name = "choropleth-gen",
    version = "0.1",
    packages = find_packages(),#['utils'],
    install_requires=['pyparsing',],
    entry_points={
        'console_scripts': [
            'gen_greyscale_choropleth=choropleth_gen.gen_greyscale_choropleth:run',
            'gen_spectral_choropleth=choropleth_gen.gen_spectral_choropleth:run',
        ],
    },

    # metadata for upload to PyPI
    author = "Luís Moreira de Sousa",
    author_email = "luis.de.sousa@protonmail.ch",
    description = "Utilities for ASCII encoded hexagonal grids",
    license = "EUPL v1.1",
    keywords = "choropleth QGis SLD",
    url = "https://github.com/ldesousa/choropleth-gen",   # project home page, if any
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: European Union Public Licence 1.1 (EUPL 1.1)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: GIS",
        ],

    # could also include long_description, download_url, classifiers, etc.
)
