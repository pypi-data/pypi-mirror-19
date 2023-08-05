import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "dmn_python",
    version = "0.1.2",
    author = "Jan Klos",
    author_email = "janklos@protonmail.com",
    description = ("Python library enabling importing and exporting a DMN model (as an XML file) and visualizating it."),
    license = "GNU GENERAL PUBLIC LICENSE",
    keywords = ["dmn", "xml"],
    url = "https://github.com/jan-klos/dmn_python",
    download_url="https://github.com/jan-klos/dmn_python/releases/download/v0.1.0/dmn_python_0.1.0.zip",
    packages=['dmn_python'],
    install_requires=[
        'lxml',
        'graphviz',
        'IPython',
        'tabulate'
    ],
    long_description=read('README.txt'),
)