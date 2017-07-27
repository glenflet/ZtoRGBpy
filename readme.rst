ZtoRGBpy Introduction
=====================
Complex number to perceptually uniform RGB subset mapping library.

This library operates on buffer object using numpy, and is designed to convert a 2d array of complex number in to an 2d array to 3-tuples of RGB values suitable for passing to matplotlibs imshow function

Requirements
------------

 * **numpy**: 1.x >= 1.6 
 * **matplotlib**: 1.x >= 1.3 or 2.x

Version Numbering
-----------------

ZtoRGBpy user a version numbering system based on PEP440_, with versions numbers ``{major:d}.{minor:d}[.{patch:d}][.dev{year:0<4d}{month:0<2d}{day:0<2d}]`` providing a minimum of major and minor version, with optional patch number for bug fixes, and development tag for pre-release builds.

Major Version
+++++++++++++
New Major Version Release, may change the public API in non backwards compatible ways, that may break existing code.

Minor Version
+++++++++++++
Minor Version, releases may add new features to the public API, but will remain fully backwards compatible with the document API for the Major Version Series.

Patch Version 
+++++++++++++
Patch are solely for fixing bugs in the code or API, these will only change the public API when it is found to perform in a manor contrary to the documented API

Development Version
+++++++++++++++++++
This is a Development release, has not be tested, it may be unstable or have breaks in the API, such a release should NOT be relied upon.

.. _PEP440: https://www.python.org/dev/peps/pep-0440/