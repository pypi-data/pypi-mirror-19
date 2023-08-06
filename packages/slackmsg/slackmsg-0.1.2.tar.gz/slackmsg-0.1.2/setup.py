'''
slackmsg setup module
'''

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
long_description = "Slack messaging CLI tool."

setup(
    name='slackmsg',
    version='0.1.2',
    description='A SlackClient wrapper command line tool',
    long_description=long_description,
    url='https://github.com/pitchdiesel/slackmsg',
    author='Gabriela Dombrowski',
    author_email='gabdombrowski@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta'
    ],

    keywords='slack slackclient wrapper command line interface',
    packages=find_packages(),
    install_requires=['docopt', 'slackclient'],
    extras_require={},
    package_data={},

    entry_points={
        'console_scripts': [
            'slackmsg=slackmsg:__main__',
        ],
    },
)
