from setuptools import setup, find_packages

setup(
    name = 'ct_fcore',
    version = '0.1.30',
    keywords = ('django', 'ctcloud', 'portal', 'ct_fcore', 'chinatelecom'),
    description = 'a portal framework for ctcloud using tornado',
    license = 'MIT License',
    install_requires = ['tornado==4.3'],

    author = 'astwyg',
    author_email = 'i@ysgh.net',
    
    packages = find_packages(),
    platforms = 'any',

    url = "https://github.com/astwyg/ct-fcore",
)