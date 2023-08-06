from setuptools import setup


def readme():
	with open('README.rst') as f:
		return f.read()


setup(name='jk_xmljsonconv',
	version='0.2017.1.17',
	description='A python module to convert XML to JSON and the other way around through a conversion manager.',
	author='Jürgen Knauth',
	author_email='pubsrc@binary-overflow.de',
	license='Apache 2.0',
	url='https://github.com/jkpubsrc/python-module-jk-xmljsonconv',
	download_url='https://github.com/jkpubsrc/python-module-jk-xmljsonconv/tarball/0.2017.1.17',
	keywords=['format-conversion', 'xml', 'json'],
	packages=['jk_xmljsonconv'],
	install_requires=[
		"jk_temporary",
		"dicttoxml",
		"xmltodict"
	],
	include_package_data=True,
	classifiers=[
		'Development Status :: 4 - Beta',
		'Programming Language :: Python :: 3.5',
		'License :: OSI Approved :: Apache Software License'
	],
	long_description=readme(),
	zip_safe=False)

