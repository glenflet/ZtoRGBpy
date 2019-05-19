..  Copyright 2019 Glen Fletcher
    This documentation is licensed under the Creative Commons Attribution-ShareAlike 4.0 International License; you may
    not use this documentation except in compliance with this License.
    You may obtain a copy of this License at: https://creativecommons.org/licenses/by-sa/4.0
    Any code samples are licensed under the Apache License, Version 2.0
    You may obtain a copy of this License at: http://www.apache.org/licenses/LICENSE-2.0

ZtoRGBpy.sRGB
=============

.. currentmodule:: ZtoRGBpy

.. py:data:: sRGB
    :annotation: = ZtoRGBpy.sRGB_HIGH

    Default sRGB Color Profile, equivalent to :py:const:`sRGB_HIGH`.

    Defined to be equal to :py:const:`sRGB_HIGH`, this defines the default color profile used
    by the mapping and plotting functions. It shouldn't be used as an explicit profile instead
    use :py:const:`sRGB_HIGH`.

    .. seealso:: :py:const:`sRGB_LOW`, :py:const:`sRGB_HIGH`

    .. rubric:: Example

    .. plot::
        :format: doctest

        Display the color wheel using matplotlib:

        >>> import matplotlib.pyplot as plt
        >>> import ZtoRGBpy
        >>> ZtoRGBpy.colorwheel(profile=ZtoRGBpy.sRGB,grid=True)
        >>> plt.show()



.. bibliography:: ..\refs.bib
    :cited:
    :style: plain
    :keyprefix: sRGB-