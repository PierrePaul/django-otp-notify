#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='django-otp-notify',
    version='0.3.0',
    description="A django-otp plugin that delivers tokens via Notify's SMS service.",
    author="Pierre-Paul Lefebvre, Peter Sagerson",
    author_email='pierre-paul.lefebvre@cds-snc.ca',
    url='https://github.com/PierrePaul/django-otp-notify',
    project_urls={
        "Documentation": 'https://django-otp-notify.readthedocs.io/',
        "Source": 'https://github.com/django-otp/django-otp-notify',
    },
    license='BSD',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
    ],

    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        'django-otp >= 0.9.0',
        'notifications-python-client',
    ],
)
