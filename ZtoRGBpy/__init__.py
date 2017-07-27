# -*- coding: utf-8 -*-
#==============================================================================
# MIT License
#
# Copyright (c) 2017 Glen Fletcher
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#==============================================================================
"""
ZtoRGBpy Module
===============

Complex number to perceptually uniform RGB subset mapping library
Supports direaction transformation of numpy arrays using remap, and
intergration with matplotlib using imshow, colorbar and colorwheel.

.. moduleauthor:: Glen Fletcher <mail@glenfletcher.com>
"""

from ZtoRGBpy._info import __authors__, __copyright__, __license__, \
                           __contact__, __version__, __title__, __desc__

from ZtoRGBpy._core import remap, Scale, LinearScale, LogScale, \
                           RGBColorProfile, sRGB_HIGH, sRGB_LOW, sRGB

try:
    from ZtoRGBpy._mpl import colorbar, colorwheel, imshow
except ImportError:
# pylint: disable=C0111
    def colorbar():
        raise NotImplementedError("Reruires Matplotlib")

    def colorwheel():
        raise NotImplementedError("Reruires Matplotlib")
    
    def imshow():
        raise NotImplementedError("Reruires Matplotlib")
