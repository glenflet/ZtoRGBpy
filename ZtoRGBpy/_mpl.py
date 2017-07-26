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
