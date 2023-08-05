from setuptools import setup, find_packages

setup(
    name = 'gentests',
    version = '1.0.0.dev1',
    description = 'A module for generating tests from data with unittest',
    url = 'https://github.com/jaredwindover/GenTests',
    author =  'Jared Windover',
    author_email = 'jaredwindover@gmail.com',
    license = 'MIT',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    keywords = 'test generation testing unit unittest data theory',
    py_modules=['gentests'],
    install_requires = [])
