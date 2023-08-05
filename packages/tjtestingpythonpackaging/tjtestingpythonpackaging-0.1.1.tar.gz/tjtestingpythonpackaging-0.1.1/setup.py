# coding: utf-8

from distutils.core import setup


def main():
	setup(
		name='tjtestingpythonpackaging',
		version='0.1.1',
		description='TJ just testing python packaging',
		author='TJ Lee',
		author_email='tj@box.com',
		packages=['tjtestingpythonpackaging'],
		download_url='https://github.com/tjlee0909/tj-testing-python-packaging/releases/tag/v0.1.1',
		install_requires=[
			'requests == 2.0',
		],
	)

if __name__ == '__main__':
	main()

