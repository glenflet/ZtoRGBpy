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
ZtoRGB core module

Provides all core functions
"""
import numpy as np

def remap(data,
          mag=1.0,
          weights=(2126.0, 7152.0, 722.0),
          igamma=2,
          return_int=False):
    """
    Convert array of complex value to RGB triples

    For 2d arrays of complex numbers the returned array is suitable
    for passing to pyplot.imshow from matplotlib.

    Parameters
    ----------
    data: array_like
        Complex input data.
    mag: None or float, optional
        Maximum magnitude, of the complex value, By default use
        the maximum magnitude of the input data. If set to a a value,
        this value is used instead, and the magnitude of the input
        will be cliped to this value.
    weights: tuple of float, optional
        Colour component weight triple for conversion to the XYZ colour space
        Defaults to (2126.0, 7152.0, 772.0), matching the sRGB colour space.
    igamma: float, optional
        Inverse gamma correction, Defaults to 2.0.
    return_int: bool
        If true returns integers in range 0-255 rather than floats in
        range 0.0-1.0, Defaults to false.
    Returns
    -------
    out: ndarray
        Array containg RGB colour values with shape z.shape + (3,),
        with the last dimention respresnting the RGB triplets.
    """
    # Get colour ratios from weights
    red_ratio = weights[0]/(weights[0]+weights[1]+weights[2])
    blue_ratio = weights[2]/(weights[0]+weights[1]+weights[2])
    # Set up trans_matrix Matrix
    chroma_limit, trans_matrix = _computeTransform(red_ratio, blue_ratio)
    lightness_cutoff = 4**(2/3.0)
    data = np.asarray(data, complex)
    magnitude = np.abs(data).reshape(*(data.shape + (1,)))
    if mag is None:
        mag = magnitude
    data = data.view(float).reshape(*(data.shape + (2,)))
    luminance = (1-(1-lightness_cutoff)*np.clip(magnitude/mag, 0, 1))**3
    chrome = chroma_limit*(1-luminance)
    rbg = np.einsum('qz,...z->...q', trans_matrix, data)
    rbg /= (magnitude > 0)*magnitude + (magnitude == 0)
    rbg *= chrome
    rbg += luminance
    rbg **= igamma
    if return_int:
        return (rbg*255).astype('i8')
    else:
        return rbg

def _computeTransform(red_ratio, blue_ratio):
    """
    Compute the trans_matrix given colour information

    Internal Use Only
    """
    blue_ratio_cuberoot = blue_ratio**(1/3.0)
    red_ratio_cuberoot = red_ratio**(1/3.0)
    # Get U, V trans_matrix based on colour ratios
    vmax = red_ratio_cuberoot/(red_ratio_cuberoot+blue_ratio_cuberoot)
    umax = blue_ratio_cuberoot/(red_ratio_cuberoot+blue_ratio_cuberoot)
    trans_matrix = np.zeros((3, 2))
    trans_matrix[0, 1] = (1-red_ratio/vmax)
    trans_matrix[1, 0] = (blue_ratio*(1-blue_ratio) /
                          (umax*(blue_ratio+red_ratio-1)))
    trans_matrix[1, 1] = (red_ratio*(1-red_ratio) /
                          (vmax*(blue_ratio+red_ratio-1)))
    trans_matrix[2, 0] = (1-blue_ratio/vmax)
    # compute set of possible chroma trans_matrix
    chroma_limit = [trans_matrix[0, 1], trans_matrix[2, 0]]
    kg2 = (trans_matrix[1, 0]**2+trans_matrix[1, 1]**2)
    chroma_limit.append(- ((trans_matrix[1, 0] + np.sqrt(kg2))*kg2 /
                           (kg2 + trans_matrix[1, 0]*np.sqrt(kg2))))
    chroma_limit.append(- ((trans_matrix[1, 0] - np.sqrt(kg2))*kg2 /
                           (kg2 - trans_matrix[1, 0]*np.sqrt(kg2))))
    # resolve overall chroma limit
    chroma_limit = 1/max(chroma_limit)
    return chroma_limit, trans_matrix