import os
from setuptools import setup, find_packages


version = '0.30'
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.rst')) as f:
    CHANGES = f.read()


setup(
    name='GreenRocket',
    version=version,
    description='A simple and compact implementation '
                'of Observer design pattern',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords='signal observer publisher subscriber asyncio',
    author='Dmitry Vakhrushev',
    author_email='self@kr41.net',
    url='https://bitbucket.org/kr41/greenrocket',
    download_url='https://bitbucket.org/kr41/greenrocket/downloads',
    license='BSD',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[],
    zip_safe=True,
)
