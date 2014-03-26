from setuptools import setup
from amonagent import __version__
 
setup(
	name='amonagent',
	version=__version__,
	description="Linux system and process information collector",
	author='Martin Rusev',
	author_email='martin@amon.cx',
	zip_safe=False,
	packages=['amonagent'],
	install_requires=['requests==2.0.0', 'unidecode'],
) 
