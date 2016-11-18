from setuptools import setup, find_packages

setup(
    name='pbs-generator',
    packages=find_packages(),
    version='1.5',
    entry_points = {
        'console_scripts': ['nicesub=pbs_generator.cli:ssh'],
    },
    install_requires=['Click', 'tabulate', 'paramiko'],
    description = 'A PBS script generator',
    author = 'Mohamad Mohebifar',
    author_email = 'mmohebifar@mun.ca',
    url = 'https://github.com/RowleyGroup/pbs-generator',
    download_url = 'https://github.com/RowleyGroup/pbs-generator/tarball/1.0',
    keywords = ['pbs-generator', 'rowley'],
    classifiers = [],
)
