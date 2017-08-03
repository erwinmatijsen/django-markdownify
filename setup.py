import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-markdownify',
    version='0.2.0',
    packages=['markdownify'],
    include_package_data=True,
    license='MIT',
    description='Markdown template filter for Django.',
    long_description=README,
    url='https://github.com/RRMoelker/django-markdownify',
    download_url='https://github.com/RRMoelker/django-markdownify/archive/0.2.0.tar.gz',
    author='R Moelker, Erwin Matijsen',
    author_email='erwin@evosites.nl',
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
