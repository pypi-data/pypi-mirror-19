import os
import sys
from setuptools import setup, find_packages

classifiers = [
	'Development Status :: 5 - Production/Stable',
	'Environment :: Win32 (MS Windows)',
	'Programming Language :: Python',
	'Programming Language :: Python :: 2.4',
	'Programming Language :: Python :: 2.5',
	'Programming Language :: Python :: 2.6',
	'Programming Language :: Python :: 2.7',
	'Intended Audience :: Developers',
	'Intended Audience :: System Administrators',
	'License :: PSF',
	'Natural Language :: English',
	'Operating System :: Microsoft :: Windows',
	'Topic :: System :: Systems Administration'
]

setup(
	name = "active_directory",
	version = "0.67.1",
	author = "Tim Golden",
	author_email = "mail@timgolden.me.uk",
	url = "http://timgolden.me.uk/python/active_directory.html",
	license = "http://www.opensource.org/licenses/mit-license.php",
	description = "Active Directory",
    long_description=open('README.md').read(),
	py_modules = ["active_directory"],
	install_requires = ["pypiwin32<=220"],
	package_data={'': ['README.md', 'ChangeLog.txt', 'TODO.txt']}
)
