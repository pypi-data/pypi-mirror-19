from setuptools import setup, find_packages
from threatconnect import __author__, __version__

setup(
    author=__author__,
    author_email='support@threatconnect.com',
    # convert_2to3_doctests = [''],
    description='Python SDK for ThreatConnect API',
    download_url='https://github.com/ThreatConnect-Inc/threatconnect-python/tarball/{}'.format(__version__),
    entry_points={
        'console_scripts': [
            'stanchion=bin.stanchion:main'
        ],
    },
    extras_require={
        ':python_version=="2.7"': ['enum34']
    },
    install_requires=['requests', 'python-dateutil'],
    license = 'Apache License, Version 2',
    name='threatconnect',
    # package_dir = {'': 'src'},
    packages=find_packages(),
    use_2to3=True,
    use_2to3_exclude_fixers=['lib2to3.fixes.fix_print'],
    # use_2to3_fixers = [''],
    url='https://github.com/ThreatConnect-Inc/threatconnect-python',
    version=__version__
)