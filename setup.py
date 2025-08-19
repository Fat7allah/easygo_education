from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

# get version from __version__ variable in easygo_education/__init__.py
from easygo_education import __version__ as version

setup(
    name="easygo_education",
    version=version,
    description="Comprehensive educational institution management system for Morocco",
    author="EasyGo Education Team",
    author_email="contact@easygo-education.ma",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
