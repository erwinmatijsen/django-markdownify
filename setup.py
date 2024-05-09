import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-markdownify',
    version='0.9.5',
    packages=['markdownify'],
    package_dir={'markdownify': 'markdownify'},
    package_data={'markdownify': ['tests/*.md']},
    include_package_data=True,
    license='MIT',
    description='Markdown template filter for Django.',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/erwinmatijsen/django-markdownify',
    download_url='https://github.com/erwinmatijsen/django-markdownify/archive/0.9.5.tar.gz',
    author='Erwin Matijsen, R Moelker',
    author_email='erwin@erwinmatijsen.nl',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'Django',
        'markdown',
        'bleach[css] >= 5.0.0',
    ],
)
