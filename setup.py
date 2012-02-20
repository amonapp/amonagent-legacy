from setuptools import setup, find_packages
 
version = "0.2"
 
setup(
    name='amonagent',
    version=version,
    description="Cross platform system and process information collector",
    author='Martin Rusev',
    author_email='martin@amon.cx',
    zip_safe=False,
	packages=find_packages(),
    install_requires=['requests'],
) 
