from setuptools import setup, find_packages
import os
path = pathroot = os.path.split(os.path.realpath(__file__))[0]


with open("README.md", "r") as fh:

    long_description = fh.read()

setup(
    name='stabby',
    version='1.0.4',
    keywords=["terminal", "ssh", "tabby like"],
    author="yombo",
    author_email="yombo@qq.com",
    url="https://github.com/Booooooger/simple_tabby",
    description="A helper for ssh operate in terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    entry_points={
        'console_scripts': ['stabby=simple_tabby.stabby:main'],
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)
