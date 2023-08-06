from setuptools import setup, find_packages

setup(
	name='django-webapp',
	version='1.0.0',
	description='Integrate a front-end webapp and build process into Django and include a new runwebapp command.',
	url='https://github.com/mvx24/django-webapp',
	author='mvx24',
	author_email='cram2400@gmail.com',
	license='MIT',
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Environment :: Console',
		'Framework :: Django',
		'License :: OSI Approved :: MIT License',
		'Operating System :: MacOS :: MacOS X',
		'Operating System :: POSIX',
		'Operating System :: Unix',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 2 :: Only',
		'Topic :: System :: Systems Administration'
	],
	keywords='webapp django html5 front-end integrated',
	packages=find_packages(),
	install_requires=['django'],
)
