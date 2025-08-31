from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

# get version from __version__ variable in olya_bootstrap/__init__.py
from olya_bootstrap import __version__ as version

setup(
    name="olya_bootstrap",
    version=version,
    description="Complete Frappe app for OLYA ESL platform",
    author="OLYA ESL",
    author_email="team@olyaesl.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)

