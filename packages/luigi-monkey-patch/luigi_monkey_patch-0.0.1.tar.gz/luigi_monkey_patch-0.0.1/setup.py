# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='luigi_monkey_patch',
    version='0.0.1',
    description='luigi monkey patch for large s3 file iteration',
    long_description=long_description,
    url='https://github.com/zenixls2/luigi_monky_patch',
    author='Zenix Huang',
    author_email='zenixls2@gmail.com',
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: System :: Monitoring',
    ],
    keywords='patch luigi s3',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['luigi'],
)
