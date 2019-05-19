..  Copyright 2019 Glen Fletcher
    This documentation is licensed under the Creative Commons Attribution-ShareAlike 4.0 International License; you may
    not use this documentation except in compliance with this License.
    You may obtain a copy of this License at: https://creativecommons.org/licenses/by-sa/4.0
    Any code samples are licensed under the Apache License, Version 2.0
    You may obtain a copy of this License at: http://www.apache.org/licenses/LICENSE-2.0

ZtoRGBpy.sRGB\_LOW
==================

.. currentmodule:: ZtoRGBpy

.. py:data:: sRGB_LOW
    :annotation: = ZtoRGBpy.RGBColorProfile((2126.0, 7152.0, 722.0), 1)

    Low Contrast sRGB Color Profile.

    Defines a low contrast color profile using gamma = :math:`1`, and color weights
    of (2126.0, 7152.0, 772.0), matching the sRGB color space defined by IEC :cite:`sRGB_LOW-IECsRGB`

    .. seealso:: :py:const:`sRGB_HIGH`, :py:const:`sRGB`

    .. rubric:: Example

    .. plot::
        :format: doctest

        Display the color wheel using matplotlib:

        >>> import matplotlib.pyplot as plt
        >>> import ZtoRGBpy
        >>> ZtoRGBpy.colorwheel(profile=ZtoRGBpy.sRGB_LOW,grid=True)
        >>> plt.show()


.. bibliography:: ..\refs.bib
    :cited:
    :style: plain
    :keyprefix: sRGB_LOW-