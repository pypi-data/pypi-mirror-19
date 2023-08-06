"""
MusicRaft
"""

#from distutils.core import setup
from setuptools import setup

setup(name = 'MusicRaft',
    version = '0.3.2',
    author = "Larry Myerscough",
    author_email='hippostech@gmail.com',
    packages=['musicraft'],
    scripts=['bin/musicraft_local.py'],
    url='http://pypi.python.org/pypi/MusicRaft/',
    license='LICENSE.txt',
    description='GUI for abcplus music notation.',
    long_description=open('README.txt').read(),
    install_requires=[
        "numpy >= 1.1.1",
        "mido >= 1.1.1",
        "PySide >= 1.1.1",

    ],
)
