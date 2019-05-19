..  Copyright 2019 Glen Fletcher
    This documentation is licensed under the Creative Commons Attribution-ShareAlike 4.0 International License; you may
    not use this documentation except in compliance with this License.
    You may obtain a copy of this License at: https://creativecommons.org/licenses/by-sa/4.0
    Any code samples are licensed under the Apache License, Version 2.0
    You may obtain a copy of this License at: http://www.apache.org/licenses/LICENSE-2.0

.. currentmodule:: ZtoRGBpy

Basic Usage
===========
This tutorial cover the general usage of :py:mod:`ZtoRGBpy`.

Mapping Complex Field to RGB data
---------------------------------
The main interface of :py:mod:`ZtoRGBpy`, is the :py:func:`remap` function which takes a
:py:class:`N dimensional Array <numpy.ndarray>` of complex values and transforms it into a
:py:class:`N+1 dimensional Array <numpy.ndarray>` of real values where the last dimension represents the RGB color
triplet. Generally, this would be used with 2D images of complex fields, or possibly 3D data cubes representing a
volumetric complex field.

Let's consider a simple complex function the cosine of the :math:`x + \iota y`::

    import ZtoRGBpy
    import numpy as np

    r = np.linspace(-5,5, 2001)
    x,y = np.meshgrid(r,r)
    z = x + 1j*y

    rgb = ZtoRGBpy.remap(np.cos(z))

This will produce a linear mapping of :math:`\cos\left(x + \iota y\right)` to the sRGB\ :cite:`usage-IECsRGB` colorspace
as described by Fletcher 2019\ :cite:`usage-fletcher2019`. The logarithmic mapping can be created by::

    rgb = ZtoRGBpy.remap(np.cos(z), scale="log")

given that the data doesn't contain a zero. For 2D data such as in the examples above the output format is suitable for
passing to matplotlib's, plotting image function :py:func:`imshow() <matplotlib.pyplot.imshow>`.

.. plot::

    import ZtoRGBpy
    import numpy as np

    r = np.linspace(-5,5, 2001)
    x,y = np.meshgrid(r,r)
    z = x + 1j*y

    rgblinear = ZtoRGBpy.remap(np.cos(z))
    rgblog = ZtoRGBpy.remap(np.cos(z), scale='log')

    import matplotlib.pyplot as plt

    plt.figure(figsize=(9,4))
    plt.subplot(121)
    plt.imshow(rgblinear, extent=[-5,5,5,-5])
    plt.subplot(122)
    plt.imshow(rgblog, extent=[-5,5,5,-5])
    plt.show()



Scaling Data
------------
The automatic scaling is perfectly good for individual fields but when there are several related fields it's important
that they are all mapped to the same scale otherwise they can't be compared directly. This can be achieved by passing
an instance of one of the scaling classes `LinearScale` or `LogScale` as the ``scale`` parameter.

`LinearScale` takes a single argument (the maximum magnitude of the scale), while `LogScale` takes
three arguments (the minimum magnitude, the maximum magnitude and the lightness limit which you can generally leave as the default).

.. plot::

    import ZtoRGBpy
    import numpy as np

    r = np.linspace(-5,5, 2001)
    x,y = np.meshgrid(r,r)
    z = x + 1j*y

    cz = np.cos(z)
    ez = np.exp(z)

    vmin = min(abs(cz).min(), abs(ez).min())
    vmax = max(abs(cz).max(), abs(ez).max())
    linear = ZtoRGBpy.LinearScale(vmax)
    log = ZtoRGBpy.LogScale(vmin, vmax)

    czlinear = ZtoRGBpy.remap(cz, scale=linear)
    czlog = ZtoRGBpy.remap(cz, scale=log)
    ezlinear = ZtoRGBpy.remap(ez, scale=linear)
    ezlog = ZtoRGBpy.remap(ez, scale=log)

    import matplotlib.pyplot as plt

    plt.figure(figsize=(9,8))
    plt.subplot(221)
    plt.imshow(czlinear, extent=[-5,5,5,-5])
    plt.subplot(222)
    plt.imshow(czlog, extent=[-5,5,5,-5])
    plt.subplot(223)
    plt.imshow(ezlinear, extent=[-5,5,5,-5])
    plt.subplot(224)
    plt.imshow(ezlog, extent=[-5,5,5,-5])
    plt.show()

Matplotlib integration
----------------------
While :py:func:`remap` is useful if you need the raw RGB data, if you just want to display an image plot of the complex
field you can use the matplotlib integrations functions :py:func:`imshow` and :py:func:`colorbar` which have been
designed to behave as similarly to the matplotlib versions as possible but applying to the plotting of complex fields.

.. plot::

    import ZtoRGBpy
    import numpy as np

    r = np.linspace(-5,5, 2001)
    x,y = np.meshgrid(r,r)
    z = x + 1j*y

    import matplotlib.pyplot as plt

    plt.figure(figsize=(9,4))
    plt.subplot(121)
    ZtoRGBpy.imshow(np.cos(z), extent=[-5,5,5,-5])
    ZtoRGBpy.colorbar()
    plt.subplot(122)
    ZtoRGBpy.imshow(np.cos(z), scale='log', extent=[-5,5,5,-5])
    ZtoRGBpy.colorbar()
    plt.show()

.. bibliography:: ..\refs.bib
   :cited:
   :style: plain
   :keyprefix: usage-