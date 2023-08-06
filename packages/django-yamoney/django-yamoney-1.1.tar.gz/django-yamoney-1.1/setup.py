import os
from setuptools import setup, find_packages
import yamoney

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-yamoney',
    version=yamoney.__version__,
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='A simple Django app for Yandex.Money service',
    long_description=README,
    author='Mpower',
    author_email='mpower.public@yandex.ru',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'Django>=1.8',
        'django-appconf>=1.0.2',
        'python-dateutil>=2.4'
    ]
)
