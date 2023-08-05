"""
    pai_parser
    ~~~~~~~~~~

    Describe and parse shell-safe strings into a structured syntax.
"""

import ast
import re

try:
    from setuptools import setup
except ImportError:
    from distutils import setup


version_regex = re.compile(r'__version__\s+=\s+(.*)')


def get_version():
    with open('pai_parser/__init__.py', 'r') as f:
        return str(ast.literal_eval(version_regex.search(f.read()).group(1)))


setup(
    name='pai-parser',
    version=get_version(),
    author='Andrew Hawker',
    author_email='andrew.r.hawker@gmail.com',
    url='https://github.com/ahawker/pai-parser',
    license='Apache 2.0',
    description='Describe and parse shell-safe strings into a structured syntax.',
    long_description=__doc__,
    packages=['pai_parser'],
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ]

)
