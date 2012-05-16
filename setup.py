# coding=utf-8
from setuptools import setup

setup(name="geogotchi",
      version="0.2.1",
      description="Library for working with geonames.org services",
      author="Simon Pantzare",
      author_email="simon+geogotchi@pewpewlabs.com",
      url="https://github.com/Memoto/geogotchi/",
      packages=["geogotchi"],
      package_dir={
          "geogotchi": "geogotchi",
          },
      license="MIT",
      platforms="Posix; MacOS X; Windows",
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Topic :: Internet",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          ],
      install_requires=[
          'requests>=0.12.1',
          ])

