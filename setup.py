import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-tempgres',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    license='Apache 2',
    description='A client for tempgres.',
    long_description=README,
    url='https://github.com/ClockworkConsulting/django-tempgres',
    author='Clockwork Consulting A/S',
    author_email='info@cwconsult.dk',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Database :: Database Engines/Servers'
    ],
)
