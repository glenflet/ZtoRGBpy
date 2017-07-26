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

class Scale(object):
    """Abstract Base for Scales"""
    def __init__(self):
        pass

    def __call__(self, value):
        """Transform value with scaling function"""
        raise NotImplementedError()

    def lmax(self):
        """Returns the maximum Lightness"""
        raise NotImplementedError()

    def ticks(self):
        """Returns a list of tick marks suitable for a colorbar"""
        raise NotImplementedError()

class LinearScale(Scale):
    """Standard Linear Scale Ranging from 0 to vmag"""
    _divisiors = [5, 10, 20, 25]
    def __init__(self, vmag=1.0):
        Scale.__init__(self)
        self.mag = float(vmag)
        self.factor = 1/self.mag

    def __call__(self, value):
        """Transform value with scaling function"""
        return value*self.factor

    def lmax(self):
        """Returns the maximum Lightness"""
        return 1

    def ticks(self):
        """Returns a list of tick marks suitable for a colorbar"""
        divisor = 0
        dfactor = 1.0
        while True:
            maxsteps = np.ceil(self.mag/(LinearScale._divisiors[divisor]
                                         *dfactor))
            if maxsteps < 4:
                if divisor == 0:
                    dfactor /= 10
                    divisor = len(LinearScale._divisiors) - 1
                else:
                    divisor -= 1
            elif maxsteps > 10:
                if divisor == len(LinearScale._divisiors) - 1:
                    dfactor *= 10
                    divisor = 0
                else:
                    divisor += 1
            else:
                break
        stepsize = LinearScale._divisiors[divisor]*dfactor
        steps = np.arange(0, self.mag, stepsize)
        offsets = steps*self.factor
        return offsets, steps

class LogScale(Scale):
    """Log Scale ranging from vmin with lightness = vLmax(0.9), to vmax"""
    def __init__(self, vmin=0.01, vmax=1.0, vLmax=0.9):
        Scale.__init__(self)
        self.logmin = np.log10(vmin)
        self.logmax = np.log10(vmax)
        self.lightness_max = vLmax
        self.lightness_buf = 1.0-vLmax
        self.factor = self.lightness_max/(self.logmax-self.logmin)

    def __call__(self, value):
        """Transform value with scaling function"""
        avalue = abs(value)
        return self.lightness_buf+(value*(np.log10(avalue) -
                                          self.logmin)/avalue)*self.factor

    def lmax(self):
        """Returns the maximum Lightness"""
        return self.lightness_max

    def ticks(self):
        """Returns a list of tick marks suitable for a colorbar"""
        logrange = int(np.ceil(self.logmax - self.logmin)) + 1
        if logrange > 6:
            pass
        else:
            steps = np.linspace(self.logmin, self.logmax, logrange)
        print steps
        offsets = self.lightness_buf+(steps - self.logmin)*self.factor
        values = 10**steps
        return offsets, values

class RGBColorProfile(object):
    """RGB Colour Profile

    weights: tuple of float, optional
        Colour component weight triple for conversion to the XYZ colour space
        Defaults to (2126.0, 7152.0, 772.0), matching the sRGB colour space.
    gamma: float, optional
        Gamma correction, Defaults to 0.5."""
    def __init__(self, weights=(2126.0, 7152.0, 722.0), gamma=0.5):
        self.weights = weights
        self.gamma = gamma

    def getRatios(self):
        """Returns Red and Blue Colour Ratios"""
        red_ratio = self.weights[0]/(self.weights[0]+
                                     self.weights[1]+self.weights[2])
        blue_ratio = self.weights[2]/(self.weights[0]+
                                      self.weights[1]+self.weights[2])
        return red_ratio, blue_ratio

    def removeGamma(self, rbg):
        """Removes gamma correction from colour"""
        return rbg ** (1.0/self.gamma)

    def applyGamma(self, rbg):
        """Applies gamma correction to colour"""
        return rbg ** self.gamma

# pylint: disable=C0103
# These constanst should start with lowercase s, as this is the correct
# usage, for writing sRGB
sRGB_HIGH = RGBColorProfile((2126.0, 7152.0, 722.0), 0.5)
sRGB_LOW = RGBColorProfile((2126.0, 7152.0, 722.0), 1)
sRGB = sRGB_HIGH
# pylint: enable=C0103

def remap(data,
          scale=LinearScale(),
          profile=sRGB,
          return_int=False):
    """
    Convert array of complex value to RGB triples

    For 2d arrays of complex numbers the returned array is suitable
    for passing to pyplot.imshow from matplotlib.

    Parameters
    ----------
    data: array_like
        Complex input data.
    scale: None or Scale object, optional
        Use to define the magnitude scaling of the data,
        data is transformed by this object to range from 0 to 1
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
    # Get colour ratios from profile
    red_ratio, blue_ratio = profile.getRatios()

    # Set up trans_matrix Matrix
    chroma_limit, trans_matrix = _computeTransform(red_ratio, blue_ratio)
    lightness_cutoff = (4**(1/3.0))/2
    data = np.asarray(data, complex)
    if scale is not None:
        data = np.asarray(scale(data), complex)
    magnitude = np.abs(data).reshape(*(data.shape + (1,)))
    #print magnitude
    data = data.view(float).reshape(*(data.shape + (2,)))
    #print data

    luminance = (1-(1-lightness_cutoff)*np.clip(magnitude, 0, 1))**3
    chrome = chroma_limit*(1-luminance)
    rbg = np.einsum('qz,...z->...q', trans_matrix, data)
    rbg /= (magnitude > 0)*magnitude + (magnitude == 0)
    rbg *= chrome
    rbg += luminance
    rbg = profile.removeGamma(rbg)
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
