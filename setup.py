from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in erpbee_english_report/__init__.py
from erpbee_english_report import __version__ as version

setup(
	name="erpbee_english_report",
	version=version,
	description="Reports which has english details in it all will be here.",
	author="LTL",
	author_email="ltl@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
