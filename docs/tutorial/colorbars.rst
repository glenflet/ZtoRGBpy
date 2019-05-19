.. Copyright 2019 Glen Fletcher
This documentation is licensed under the Creative Commons Attribution-ShareAlike 4.0 International License; you may
not use this documentation except in compliance with this License.
You may obtain a copy of this License at: https://creativecommons.org/licenses/by-sa/4.0
Any code samples are licensed under the Apache License, Version 2.0
You may obtain a copy of this License at: http://www.apache.org/licenses/LICENSE-2.0

Using Colorbars
===============
While the `ZtoRGBpy.colorbar <colorbar>` behaves similarly to `pyplot.colorbar <matplotlib.pyplot.colorbar>`, its
behaviour is subtly different. This difference is noticeable when plotting several subplots using different colorbars.

.. plot::

     import ZtoRGBpy
     import numpy as np
     import matplotlib.pyplot as plt

     r = np.linspace(-5,5, 2001)
     x,y = np.meshgrid(r,r)
     z = x + 1j*y

     plt.figure(figsize=(9,4))
     plt.subplot(121)
     ZtoRGBpy.imshow(np.cos(z), extent=[-5, 5, 5, -5])
     ZtoRGBpy.colorbar()
     plt.subplot(122)
     plt.imshow(abs(np.cos(z)), cmap='hot', extent=[-5, 5, 5, -5])
     plt.colorbar()
     plt.show()

This occurs because `ZtoRGBpy` draws the colorbar by using imshow with ``aspect='auto'``, thus the solution
is to set the aspect ratio of the normal colorbar to auto as well. This can be done as:

.. plot::

     import ZtoRGBpy
     import numpy as np
     import matplotlib.pyplot as plt

     r = np.linspace(-5,5, 2001)
     x,y = np.meshgrid(r,r)
     z = x + 1j*y

     plt.figure(figsize=(9,4))
     plt.subplot(121)
     ZtoRGBpy.imshow(np.cos(z), extent=[-5, 5, 5, -5])
     ZtoRGBpy.colorbar()
     plt.subplot(122)
     plt.imshow(abs(np.cos(z)), cmap='hot', extent=[-5, 5, 5, -5])
     plt.colorbar().ax.set_aspect('auto')
     plt.show()
