"""
XDocs
"""
import codecs
import os
import re

from setuptools import find_packages
from setuptools import setup

with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'xdocs', '__init__.py'), 'r', 'latin1') as fp:
    try:
        version = re.findall(r"^__version__ = '([^']+)'\r?$",
                             fp.read(), re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')
long_description = (
    "XDocs is a fast and simple documentation generator "
    "that's geared towards building project documentation. Documentation "
    "source files are written in YAML, and configured with a single YAML "
    "configuration file."
)
setup(
    name='xdocs',
    version=version,
    license='MIT',
    description='Documentation drives developing.',
    long_description=long_description,
    author='gaojiuli',
    author_email='gaojiuli@gmail.com',
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Faker>=0.7.7',
        "click>=6.7",
        'livereload>=2.5.1',
        'bottle>=0.12.13',
        'PyYAML>=3.12'],
    url='https://github.com/gaojiuli/XDocs',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'xdocs=xdocs.__main__:cli',
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Programming Language :: Python :: Implementation :: CPython",
        'Topic :: Documentation',
        'Topic :: Text Processing',
    ],
    zip_safe=False,
)
