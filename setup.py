from setuptools import setup, find_packages
import os

# Read requirements
with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# Get version from __version__ variable in aspirehr/__init__.py
version_file = os.path.join(os.path.dirname(__file__), "aspirehr", "__init__.py")
with open(version_file, "r") as f:
	exec(f.read())

setup(
	name="aspirehr",
	version=__version__,
	description="Modern HR and Payroll Management System",
	author="Your Company",
	author_email="admin@yourcompany.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
