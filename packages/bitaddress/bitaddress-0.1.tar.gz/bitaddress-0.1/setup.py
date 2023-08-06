from setuptools import setup, find_packages

setup(name='bitaddress',
	version='0.1',
	description='Generate bitcoin addresses',
	url='https://github.com/pta2002/bitaddress',
	author='Pedro Alves',
	author_email='pta2002@pta2002.com',
	license='MIT',
	packages=find_packages(),
	install_requires=[
		'ecdsa'
	])