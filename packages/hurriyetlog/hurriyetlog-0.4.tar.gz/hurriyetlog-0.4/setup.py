from setuptools import setup

setup(
    name="hurriyetlog",                  # This is the name of your PyPI-package.
    description="hurriyet python log",   # Description
    version="0.4",                       # Update the version number for new releases
    author="hurriyet.com.tr",
    author_email="destek@hurriyet.com.tr",
    scripts=["hurriyetlog"],             # The name of your scipt, and also the command you'll be
    license="MIT",
    url="http://www.hurriyet.com.tr",
    install_requires=["socket"]
)
