from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in aspirehr/__init__.py
from aspirehr import __version__ as version

setup(
	name="aspirehr",
	version=version,
	description="Modern HR and Payroll Management System",
	author="Your Company",
	author_email="admin@yourcompany.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
