# from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name='eurotools',
    version='0.1.0',
    packages=find_packages(),
    license='',
    long_description=open('README.rst').read(),
    url='http://www.stoneworksolutions.net',
    author='Antonio Palomo Cardenas',
    author_email='antonio.palomo@stoneworksolutions.net',
    package_data={'': ['*.html']},
    include_package_data=True,
    install_requires=[],
)
