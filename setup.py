# coding: utf-8
import os
from setuptools import setup, find_packages
import re
import sys


def get_version(package):
    """
    Return package version as listed in `__version__` in `__init__.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search(
        "^__version__ = ['\"]([^'\"]+)['\"]",
        init_py, re.MULTILINE).group(1)

version = get_version('object_feedback')

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    args = {'version': version}
    print("You probably want to also tag the version now:")
    print("  git tag -a %(version)s -m 'version %(version)s'" % args)
    print("  git push --tags")
    sys.exit()

setup(
    name="django-object-feedback",
    version=version,
    author="Felipe Martín",
    author_email="fmartingr@me.com",
    description="A simple django app to allow feedback on model instances.",
    license="GPLv2",
    keywords="django feedback",
    url="https://github.com/fmartingr/django-object-feedback",
    include_package_data=True,
    packages=find_packages(),
    install_requires=open('requirements.txt').read().split('\n'),
    long_description='README.md',
    classifiers=[
        'Development Status :: 3 - Alpha',
    ],
)
