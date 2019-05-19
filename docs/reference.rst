.. Copyright 2019 Glen Fletcher
This documentation is licensed under the Creative Commons Attribution-ShareAlike 4.0 International License; you may
not use this documentation except in compliance with this License.
You may obtain a copy of this License at: https://creativecommons.org/licenses/by-sa/4.0
Any code samples are licensed under the Apache License, Version 2.0
You may obtain a copy of this License at: http://www.apache.org/licenses/LICENSE-2.0

.. automodule:: ZtoRGBpy

    Plotting Functions
    ------------------
    .. autosummary::
        :toctree: reference/

        imshow
        colorbar
        colorwheel

    ..

    Color Mapping Functions
    -----------------------
    .. autosummary::
        :toctree: reference/

        remap

    ..

    Scaling Classes
    ---------------
    .. autosummary::
        :toctree: reference/

        Scale
        LinearScale
        LogScale

    ..

    RGB Color Profiles
    ------------------
    .. toctree::
        :hidden:

        reference/ZtoRGBpy.RGBColorProfile.rst
        reference/ZtoRGBpy.sRGB_LOW.rst
        reference/ZtoRGBpy.sRGB_HIGH.rst
        reference/ZtoRGBpy.sRGB.rst

    ===========================================  ================================================================================================================================================================
    :obj:`RGBColorProfile`\ ([weights, gamma])   Defines a color profile in a given RGB color spaceby conversion factors for red, green and blue to the Y component of the XYZ color space, i.e. the white point.
    :obj:`sRGB_LOW`                              Low Contrast sRGB Color Profile.
    :obj:`sRGB_HIGH`                             High Contrast sRGB Color Profile.
    :obj:`sRGB`                                  Default sRGB Color Profile, Equivalent to `sRGB_HIGH`.
    ===========================================  ================================================================================================================================================================


.. bibliography:: refs.bib
    :cited:
    :style: plain
    :keyprefix: module-
