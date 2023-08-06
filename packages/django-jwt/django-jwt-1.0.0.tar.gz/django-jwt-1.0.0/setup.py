import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as readme:
	README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name='django-jwt',
    version='1.0.0',
    license='MIT',
    packages=['django_jwt'],
    include_package_data=True,
    description='JWT implementation for Django and Django Rest Framework',
    long_description=README,
    url='https://github.com/ah450/django-jwt',
    author='Ahmed Hisham Ismail',
    author_email= 'ahm3d.hisham@gmail.com',
    zip_safe=True,
    classifiers=[
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License'
    ],
    install_requires=['python-jose >= 1.3', 'django >= 1.10'],
    extras_require={
        'drf': ['djangorestframework >= 3.5']
    } 
)