from distutils.core import setup
from setuptools import find_packages
from send_html_email import VERSION


setup(
name='send-html-email',
description='Sends an html email that populates a template with and object, dictionary or both',
author='Level Up',
author_email='os@lvlup.us',
version=VERSION,
packages=find_packages(),
license='GPL v3',
long_description=open('README.txt').read(),
include_package_data=True,
)
