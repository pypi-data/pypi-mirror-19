from setuptools import setup, find_packages

setup(
    name='xdocs',
    version='0.1.8',
    license='MIT',
    description='Documentation drives developing.',
    author='gaojiuli',
    author_email='gaojiuli@gmail.com',
    include_package_data=True,
    install_requires=[
        'faker',
        "click",
        'livereload',
        'bottle'],
    url='https://github.com/gaojiuli/Xdocs',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'xdocs=xdocs.__main__:cli',
        ],
    },
)
