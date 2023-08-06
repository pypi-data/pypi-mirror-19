# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function

from setuptools import setup

# Hmmmph.
# So we get all the meta-information in one place (yay!) but we call
# exec to get it (boo!). Note that we can't "from txtorcon._metadata
# import *" here because that won't work when setup is being run by
# pip (outside of Git checkout etc)
with open('pylioness/_metadata.py') as f:
    exec(
        compile(f.read(), '_metadata.py', 'exec'),
        globals(),
        locals(),
    )

description = '''
    python lioness block cipher
'''

setup(
    name='pylioness',
    version=__version__,
    description=description,
    keywords=['python', 'cryptography'],
    install_requires=open('requirements.txt').readlines(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Security :: Cryptography',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    author=__author__,
    author_email=__contact__,
    url=__url__,
    license=__license__,
    packages=["pylioness"],
)
