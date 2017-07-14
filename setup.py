"""
Setup script.
"""

from distutils.core import Command
from setuptools import setup


class Coverage(Command):
    """
    Coverage setup.
    """

    description = (
        "Run test suite against single instance of"
        "Python and collect coverage data."
    )
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import coverage
        import unittest

        cov = coverage.coverage(config_file='.coveragerc')
        cov.erase()
        cov.start()

        test_loader = unittest.TestLoader()
        test_suite = test_loader.discover(start_dir='tests')
        unittest.TextTestRunner().run(test_suite)

        cov.stop()
        cov.save()
        cov.report()
        cov.html_report()


setup(
    author='Mohamad Mohebifar',
    author_email='mmohebifar@mun.ca',
    description='A declarative python library for generating and submitting' +
    'jobs to different queueing systems e.g. Slurm, Torque, etc.',
    download_url='',
    cmdclass={
        'coverage': Coverage,
    },
    install_requires=[
    ],
    license='GNU GPL (3.0)',
    name='pyqueue',
    packages=[
        'pyqueue',
    ],
    scripts=[],
    test_suite='tests',
    tests_require=[
        'codecov>=2.0.3,<3.0.0',
        'coverage>=4.0.3,<5.0.0',
        'Sphinx>=1.4.1,<2.0.0',
        'tox>=2.3.1,<3.0.0',
        'virtualenv>=15.0.1,<16.0.0'
    ],
    url='',
    version='1.0.0'
)
