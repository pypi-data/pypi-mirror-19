from setuptools import find_packages, setup

from powerplug.version import __version__

setup(
    name='powerplug',
    version=__version__,
    author='Paul Traylor',
    url='https://github.com/kfdm/django-powerplug',
    packages=find_packages(exclude=['test']),
    install_requires=[
        'Django',
    ],
    entry_points={
        'powerplug.apps': [
            'powerplug = powerplug',
        ],
    }
)
