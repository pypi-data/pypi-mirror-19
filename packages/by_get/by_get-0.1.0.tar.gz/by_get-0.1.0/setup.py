# -*- coding: utf-8 -*-
"""Setup routine of by_get.

.. moduleauthor:: Florian Aldehoff <by_get@biohazardous.de>
"""

# Work around mbcs bug in distutils. See http://bugs.python.org/issue10945
import codecs
try:
    codecs.lookup('mbcs')
except LookupError:
    ASCII = codecs.lookup('ascii')
    MBCS = lambda name, enc=ASCII: {True: enc}.get(name == 'mbcs')
    codecs.register(MBCS)

from setuptools import setup

# custom libraries
from by_get.version import VERSION


def readme():
    """Get contents of ReST documentation."""
    with open('README.rst') as file:
        return file.read()

setup(
    name='by_get',
    version=VERSION,
    description='BY image getter',
    long_description=readme(),
    # see full list at https://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search'
    ],
    url='http://pypi.python.org/pypi/by_get/',
    author='Florian Aldehoff',
    author_email='by_get@biohazardous.de',
    license='LICENSE.txt',
    packages=[
        'by_get'
    ],
    entry_points={
        'console_scripts': [
            'by_get=by_get.by_get:main'
        ]
    },
    install_requires=[
        'requests >= 2.4.3',
        'pytest >= 2.6.3'
    ],
    zip_safe=False
)
