from setuptools import setup, find_packages

long_description = (
    "XDocs is a fast and simple documentation generator "
    "that's geared towards building project documentation. Documentation "
    "source files are written in YAML, and configured with a single YAML "
    "configuration file."
)
setup(
    name='xdocs',
    version='0.2.4',
    license='MIT',
    description='Documentation drives developing.',
    long_description=long_description,
    author='gaojiuli',
    author_email='gaojiuli@gmail.com',
    include_package_data=True,
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
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        "Programming Language :: Python :: Implementation :: CPython",
        'Topic :: Documentation',
        'Topic :: Text Processing',
    ],
    zip_safe=False,
)
