# -*- coding: utf-8 -*-

from setuptools import setup

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name="4chan",
    packages=["chan"],
    entry_points={
        "console_scripts": ['chan = chan.chan:main']
    },
    version='0.0.2',
    description="A python script that downloads all images from a 4chan thread.",
    long_description=long_descr,
    author="Anthony Bloomer",
    author_email="ant0@protonmail.ch",
    url="https://github.com/AnthonyBloomer/chan"

)