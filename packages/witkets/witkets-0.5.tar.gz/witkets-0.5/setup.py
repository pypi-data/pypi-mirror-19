import sys
from setuptools import setup, find_packages
from witkets import __version__

setup(  
    name = "witkets",
    version = __version__,
    description = "Tkinter extensions",
    packages = find_packages(),
	author = 'Leandro Mattioli',
	author_email = 'leandro.mattioli@gmail.com',
	url='http://www.pythonhosted.org/witkets',
	license='LGPL'
)
