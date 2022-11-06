from setuptools import setup, find_packages
import os
path = pathroot = os.path.split(os.path.realpath(__file__))[0]


with open("README.md", "r") as fh:

    long_description = fh.read()

setup(
    name='stabby',
    version='0.1.0',
    author="<authorname>",
    author_email="<authorname@templatepackage.com>",
    description="Simple tool like tabby",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "pyperclip==1.8.2",
        "prettytable==3.5.0",
        "wcwidth==0.2.5"
    ],
    entry_points={
        'console_scripts': ['stabby=simple_tabby.terminal:main'],
    },
)
