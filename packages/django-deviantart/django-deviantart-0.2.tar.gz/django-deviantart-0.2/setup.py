import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

requirements = [
    'requests_oauthlib'
]

setup(
    name='django-deviantart',
    version='0.2',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    install_requires=requirements,
    description='Deviantart API (OAuth2) for your django project',
    long_description=README,
    url='https://pierre.isartistic.biz/',
    author='Pierre Geier',
    author_email='pierre@isartistic.biz',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
