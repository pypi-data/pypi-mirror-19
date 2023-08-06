from setuptools import setup

setup(
    name = 'pyTrivialFTP',
    version = '0.2.0',
    description = "The poor man's API for accessing data on a remote FTP repository",
    py_modules = [ 'pyTrivialFTP' ],
    author = 'Roberto Reale',
    author_email = 'roberto.reale@linux.com',
    url = 'https://github.com/robertoreale/pyTrivialFTP',
    keywords = [ 'FTP' ],
    install_requires = [ 
    'FTP',
    ]
)
