import codecs
import os
import re
from setuptools import setup, find_packages


PACKAGE_NAME = 'scythe'
PACKAGE_DIR = os.path.dirname(__file__)


def read(fname):
    with codecs.open(fname, 'r', encoding='utf-8') as f:
        return f.read()


def get_version(package):
    init_py_path = os.path.join(package, '__init__.py')
    init_py = read(init_py_path)
    # __version__ isn't set, this will error out
    version = re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)
    return version


setup(
    name='scythe-game',
    version=get_version(PACKAGE_NAME),
    author="Chuck Bassett",
    author_email="iamchuckb@gmail.com",
    description="Modeling the boardgame Scythe",
    license="MIT",
    url="https://github.com/chucksmash/scythe.git",
    keywords="scythe boardgames",
    packages=find_packages(exclude=["tests", "docs"]),
    long_description=read("README.md"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    install_requires=[],
    zip_safe=False
)
