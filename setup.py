from setuptools import setup, find_packages
import os
path = pathroot = os.path.split(os.path.realpath(__file__))[0]


with open("README.md", "r") as fh:

    long_description = fh.read()

setup(
    name='stabby',
    version='1.0.1',
    author="yombo",
    author_email="",
    url="https://github.com/Booooooger/simple_tabby",
    description="A helper for ssh operate in terminal",
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
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)
