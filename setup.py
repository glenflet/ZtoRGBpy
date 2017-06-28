# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 00:30:51 2014

.. moduleauthor:: Glen Fletcher <glen.fletcher@alphaomega-technology.com.au>
"""
from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages
import os.path
import re

pkg_name = 'ZtoRGBpy'
pkg = {}
with open(os.path.join(pkg_name,'_info.py')) as f: exec(f.read(),pkg,pkg)

reimg = re.compile("^!\[(?P<label>[^\]]*)\]\((?P<src>[^\)]*)\)$")
relink = re.compile("\[(?P<label>[^\]]*)\]\((?P<href>[^\)]*)\)")
reimglink = re.compile(
"^\[!\[(?P<label>[^\]]*)\]\((?P<src>[^\)]*)\)\]\((?P<href>[^\)]*)\)$")

def read(fname):
    """Read Markdown File And Convert to reST"""
    imgindex = 0
    lines = ""
    for line in open(os.path.join(os.path.dirname(__file__), fname),'rt'):
        m = reimg.match(line)
        if m is not None:
            g = m.groupdict()
            if g['label'] is None:
                g['label'] = 'image' + imgindex
                imgindex += 1
            lines = "|{label:s}|\n\n.. |{label:s}| image:: {src:s}\n".format(
                        **g)
            continue
        m = reimglink.match(line)
        if m is not None:
            g = m.groupdict()
            if g['label'] is None:
                g['label'] = 'image' + imgindex
                imgindex += 1
            lines += "|{label:s}|\n\n.. |{label:s}| image:: {src:s}\n"\
                "   :target: {href:s}".format(**g)
            continue
        if line[0:5] == "Note:":
            line = ".. Note::" + line[5:]
        line = relink.sub('`\g<label> <\g<href>>`_',line)
        lines += line
    return lines

def readlist(fname):
    return open(os.path.join(
        os.path.dirname(__file__),
        fname),'rt').read().split('\n')


setup(
    name=pkg['__title__'],
    version=pkg['__version__'],
    author=pkg['__authors__'][0][0],
    author_email=pkg['__authors__'][0][1],
    license=pkg['__license__'],
    description=pkg['__desc__'],
    packages=find_packages(),
    url='https://github.com/glenflet/' + pkg['__title__'],
    long_description=read('README.md'),
    install_requires = ['numpy>=1.6,<2', 'matplotlib>=1.3,<3'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics",
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License"
    ],
    zip_safe=True,
)
