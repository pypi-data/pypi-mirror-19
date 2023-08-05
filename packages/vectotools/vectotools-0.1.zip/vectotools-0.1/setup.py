from setuptools import setup
from setuptools import find_packages
VERSION = __import__("vector").__version__

setup(
    packages=find_packages(),
    name='vectotools',
    version=VERSION,
    author='Ddone',
    author_email='mynameisthenekit@gmail.com',
    license='MIT',
    description=('Simple 2D vector library'),
    long_description=open('README.rst').read(),
    keywords='simple vector algebra',
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3'
    ],
)

