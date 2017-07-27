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
ZtoRGB Matplotlib Module

Provides extenstion functuons for matplotlib
"""
import matplotlib.pyplot as plt
import matplotlib.colorbar as cbar
from matplotlib.axes import SubplotBase
import numpy as np
from ZtoRGBpy._core import remap, LinearScale, sRGB

def colorbar(ax=None, cax=None, use_gridspec=True,
             scale=LinearScale(1.0), profile=sRGB, **kw):
    """Generate a Matplotlib Colorbar

    Renders a special colorbar showing phase rotation on the oppsite
    axis to the magnitude (no axis labels)
    """
    current_ax = plt.gca()
    if cax is None:
        if ax is None:
            ax = current_ax
        if use_gridspec and isinstance(ax, SubplotBase):
            cax, kw = cbar.make_axes_gridspec(ax, **kw)
        else:
            cax, kw = cbar.make_axes(ax, **kw)
    phase = np.linspace(-np.pi, np.pi, 45)
    magnitude = np.linspace(1, 0, 1000)
    phase, magnitude = np.meshgrid(phase, magnitude)
    z_cb = cax.imshow(remap(magnitude*np.exp(1j*phase),
                            profile=profile),
                      aspect="auto",
                      extent=[0, np.pi*2, 0, 1.0])
    cax.xaxis.set_visible(False)
    cax.yaxis.tick_right()
    ticks = scale.ticks()
    ticks = cax.set_yticks(ticks[0]), cax.set_yticklabels(ticks[1])
    cax.yaxis.set_ticks_position("right")
    cax.yaxis.set_label_position("right")
    plt.sca(current_ax)
    return z_cb, cax

def colorwheel(ax=None, scale=LinearScale(1.0), profile=sRGB,
               rotation=0, grid=False):
    """Generate a Colorwheel

    Renders a colorwheel, showing the colorspace, with optional grid
    """
    rline = np.linspace(-1, 1, 1001)
    xmesh, ymesh = np.meshgrid(rline, rline)
    zmesh = xmesh+1j*ymesh
    zmesh *= np.exp(1j*rotation)
    rgba = np.ones(zmesh.shape + (4,))
    rgba[..., 3] = abs(zmesh) <= 1
    rgba[..., 0:3] = remap(zmesh, profile=profile)
    current_ax = plt.gca()
    if ax is None:
        ax = current_ax
    z_im = ax.imshow(rgba, extent=[-1, 1, 1, -1])
    ax.axis('off')
    if grid:
        pax = ax.figure.add_axes(ax.figbox, projection='polar', frameon=False)
        ticks = scale.ticks()
        ticks = pax.set_rticks(ticks[0]), pax.set_yticklabels(ticks[1])
        pax.set_theta_zero_location("N")
        pax.set_rlabel_position(290)
        pax.yaxis.grid(True, which='major', linestyle='-')
        pax.xaxis.grid(True, which='major', linestyle='-')
    else:
        pax = None
    plt.sca(current_ax)
    return z_im, pax

def imshow(Z, ax=None, scale=None, profile=sRGB, **kwargs):
    """imshow(Z, ax=None, scale=None, profile=sRGB, aspect=None, \
    interpolation=None, alpha=None, origin=None, extent=None, shape=None, \
    filternorm=1, filterrad=4.0, **kwargs)
    Display a complex image on the ax or the current axes.
    
    Parameters
    ----------
    Z : array_like, shape(n, m)
        Display the complex data `Z` to ax or current axes.
        Arrays are mapped to colors based on
        ZtoRGBpy.remap(Z, scale=scale, profile=profile)
        
    ax : axes, optional, default: None
        The axes to plot to, use the current axes like pyplot.imshow, if None
        
    scale : Scale, optional, default: None
        The data scaling, if None, scale is choose to be a linear scale with
        magnitude equal to abs(Z), i.e. LinearScale(abs(Z))
        
    profile : RGBColorProfile, optional, default: sRGB
        The color profile to use for mapping Complex data to RGB
        
    aspect : ['auto' | 'equal' | scalar], optional, default: None
        If 'auto', changes the image aspect ratio to match that of the
        axes.
    
        If 'equal', and `extent` is None, changes the axes aspect ratio to
        match that of the image. If `extent` is not `None`, the axes
        aspect ratio is changed to match that of the extent.
    
        If None, default to rc ``image.aspect`` value.
        
    interpolation : string, optional, default: None
        Acceptable values are 'none', 'nearest', 'bilinear', 'bicubic',
        'spline16', 'spline36', 'hanning', 'hamming', 'hermite', 'kaiser',
        'quadric', 'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc',
        'lanczos'
    
        If `interpolation` is None, default to rc `image.interpolation`.
        See also the `filternorm` and `filterrad` parameters.
        If `interpolation` is 'none', then no interpolation is performed
        on the Agg, ps and pdf backends. Other backends will fall back to
        'nearest'.
        
    alpha : scalar, optional, default: None
        The alpha blending value, between 0 (transparent) and 1 (opaque)
    
    origin : ['upper' | 'lower'], optional, default: None
        Place the [0,0] index of the array in the upper left or lower left
        corner of the axes. If None, default to rc `image.origin`.
    
    extent : scalars (left, right, bottom, top), optional, default: None
        The location, in data-coordinates, of the lower-left and
        upper-right corners. If `None`, the image is positioned such that
        the pixel centers fall on zero-based (row, column) indices.
    
    shape : scalars (columns, rows), optional, default: None
        For raw buffer images
    
    filternorm : scalar, optional, default: 1
        A parameter for the antigrain image resize filter.  From the
        antigrain documentation, if `filternorm` = 1, the filter
        normalizes integer values and corrects the rounding errors. It
        doesn't do anything with the source floating point values, it
        corrects only integers according to the rule of 1.0 which means
        that any sum of pixel weights must be equal to 1.0.  So, the
        filter function must produce a graph of the proper shape.
    
    filterrad : scalar, optional, default: 4.0
        The filter radius for filters that have a radius parameter, i.e.
        when interpolation is one of: 'sinc', 'lanczos' or 'blackman'
    """
    current_ax = plt.gca()
    if ax is None:
        ax = current_ax
    z_im = ax.imshow(remap(Z, scale=scale, profile=profile), **kwargs)
    # add meta data so ZtoRGBpy.colorbar can pull
    #   scale and profile automatically
    z_im.ZtoRGBpy_meta = {"scale": scale, "profile": profile}
    plt.sca(current_ax)
    return z_im
