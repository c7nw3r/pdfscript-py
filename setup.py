import os
# read the contents of your README file
from pathlib import Path

import pkg_resources
from setuptools import find_packages, setup

long_description = Path(__file__).with_name("README.md").read_text()

setup(
    name='pdfscript-py',
    packages=find_packages(exclude=("test")),
    version='0.1.0',
    license='Apache Software License',
    description='tbd',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='c7nw3r',
    url='https://github.com/c7nw3r/pdfscript-py',
    download_url='https://github.com/c7nw3r/pdfscript-py/archive/refs/tags/v0.1.0.tar.gz',
    setup_requires=['setuptools_scm'],
    include_package_data=True,
    install_requires=[
        str(r)
        for r in pkg_resources.parse_requirements(
            open(os.path.join(os.path.dirname(__file__), "requirements.txt"))
        )
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
    ],
    extras_require={
    }
)
