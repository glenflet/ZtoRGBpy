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
from ZtoRGB.core import remap

def colorbar(ax=None, cax=None, use_gridspec=True,
             vmin=0, vmax=1, scale='linear', **kw):
    """
    Generate a Matplotlib Colorbar

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
    rgb = remap(magnitude*np.exp(1j*phase))
    z_cb = cax.imshow(rgb, aspect="auto", extent=[0, np.pi*2, vmin, vmax])
    cax.set_yscale(scale)
    cax.xaxis.set_visible(False)
    cax.yaxis.tick_right()
    cax.yaxis.set_ticks_position("right")
    cax.yaxis.set_label_position("right")
    plt.sca(current_ax)
    return z_cb, cax
