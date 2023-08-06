pyzbar
======

|Python Versions| |PyPI version| |Travis status| |Coverage Status|

A ``ctypes``-based Python wrapper around the
`zbar <http://zbar.sourceforge.net/>`__ barcode reader.

The
`zbar <https://sourceforge.net/p/zbar/code/ci/default/tree/python/>`__
wrapper is stuck in Python 2.x-land. The
`zbarlight <https://github.com/Polyconseil/zbarlight/>`__ wrapper
doesn't provide support for Windows and depends upon Pillow. This
``ctypes``-based wrapper brings ``zbar`` to Python 2.7 and to Python 3.4
or greater.

Installation
------------

The ``zbar`` ``DLL``\ s are included with the Windows Python wheels. On
other operating systems, you will need to install the ``zbar`` shared
library.

On Mac OS X:

::

    brew install zbar

On Linux:

::

    sudo apt-get install libzbar0

Install this Python wrapper; use the second form to install dependencies
of the command-line scripts:

::

    pip install pyzbar
    pip install pyzbar[scripts]

Example usage
-------------

The ``decode`` function accepts instances of ``PIL.Image``.

::

    >>> from pyzbar.pyzbar import decode
    >>> from PIL import Image
    >>> decode(Image.open('pyzbar/tests/code128.png'))
    [Decoded(data=b'Foramenifera', type='CODE128'),
     Decoded(data=b'Rana temporaria', type='CODE128')]

It also accepts instances of ``numpy.ndarray``, which might come from
loading images using `OpenCV <http://opencv.org/>`__.

::

    >>> import cv2
    >>> decode(cv2.imread('pyzbar/tests/code128.png'))
    [Decoded(data=b'Foramenifera', type='CODE128'),
     Decoded(data=b'Rana temporaria', type='CODE128')]

You can also provide a tuple ``(pixels, width, height)``, where the
image data is eight bits-per-pixel.

::

    >>> image = cv2.imread('pyzbar/tests/code128.png')
    >>> height, width = image.shape[:2]

    >>> # 8 bpp by considering just the blue channel
    >>> decode((image[:, :, 0].astype('uint8').tobytes(), width, height))
    [Decoded(data=b'Foramenifera', type='CODE128'),
     Decoded(data=b'Rana temporaria', type='CODE128')]

    >>> # 8 bpp by converting image to greyscale
    >>> grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    >>> decode((grey.tobytes(), width, height))
    [Decoded(data=b'Foramenifera', type='CODE128'),
     Decoded(data=b'Rana temporaria', type='CODE128')]

    >>> # If you don't provide 8 bpp
    >>> decode((image.tobytes(), width, height))
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/Users/lawh/projects/pyzbar/pyzbar/pyzbar.py", line 102, in decode
        raise PyZbarError('Unsupported bits-per-pixel [{0}]'.format(bpp))
    pyzbar.pyzbar_error.PyZbarError: Unsupported bits-per-pixel [24]

``zbar``'s default behaviour is (I think) to decode all symbol types.
You can ask ``zbar`` to look for just your symbol types (I have no idea
of the effect of this on performance)

::

    >>> from pyzbar.pyzbar import ZBarSymbol
    >>> # Look for just qrcode
    >>> decode(Image.open('pyzbar/tests/qrcode.png'), symbols=[ZBarSymbol.QRCODE])
    [Decoded(data=b'Thalassiodracon', type='QRCODE')]

    >>> # If we look for just code128, the qrcodes in the image will not be detected
    >>> decode(Image.open('pyzbar/tests/qrcode.png'), symbols=[ZBarSymbol.CODE128])
    []

License
-------

``pyzbar`` is distributed under the MIT license (see ``LICENCE.txt``).
The ``zbar`` shared library is distributed under the GNU Lesser General
Public License, version 2.1 (see ``zbar-LICENCE.txt``).

.. |Python Versions| image:: https://img.shields.io/badge/python-2.7%2C%203.4%2C%203.5%2C%203.6-blue.svg
   :target: https://github.com/NaturalHistoryMuseum/pyzbar
.. |PyPI version| image:: https://badge.fury.io/py/pyzbar.svg
   :target: https://pypi.python.org/pypi/pyzbar/
.. |Travis status| image:: https://travis-ci.org/NaturalHistoryMuseum/pyzbar.svg?branch=master
   :target: https://travis-ci.org/NaturalHistoryMuseum/pyzbar
.. |Coverage Status| image:: https://coveralls.io/repos/github/NaturalHistoryMuseum/pyzbar/badge.svg?branch=master
   :target: https://coveralls.io/github/NaturalHistoryMuseum/pyzbar?branch=master


