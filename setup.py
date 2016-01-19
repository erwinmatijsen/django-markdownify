import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-markdownify',
    version='0.1.0',
    packages=['markdownify'],
    include_package_data=True,
    license='MIT',
    description='Markdown template filter for Django.',
    long_description=README,
    url='https://github.com/RRMoelker/django-markdownify',
    author='R Moelker',
    author_email='r@m.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'Django',
        'markdown',
        'bleach',
    ],
)
