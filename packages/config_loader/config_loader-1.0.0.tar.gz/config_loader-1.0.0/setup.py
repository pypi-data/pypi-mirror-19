#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools

__version__ = "1.0.0"

install_requires = [
    'PyYAML>=3.10',
]

setuptools.setup(
    name="config_loader",
    version=__version__,
    description="Module that manage configurations",
    url="https://github.com/ateliedocodigo/py-config_loader",
    author="Luis Fernando Gomes",
    author_email="luiscoms@ateliedocodigo.com.br",
    license="MIT",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
    ],
    keywords="yml yaml config file",
    packages=setuptools.find_packages('src'),
    # setup_requires=[
    #     "PyYAML==3.12"
    # ],
    # include_package_data=True,
    # zip_safe=False,
    test_suite="tests",
    install_requires=install_requires,
    python_requires='>=2.7',
    # zip_safe=False,
    package_dir={'config_loader': 'src'}
)
