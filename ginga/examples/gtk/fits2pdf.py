#! /usr/bin/env python
#
# fits2pdf.py -- Image a FITS file as a PDF.
#
# This is open-source software licensed under a BSD license.
# Please see the file LICENSE.txt for details.
#
"""
To run this script::

    $ ./fits2pdf.py <fitsfile> <output.pdf>

"""

import logging
import sys
from optparse import OptionParser

import cairo

from ginga.cairow.ImageViewCairo import ImageViewCairo
from ginga.AstroImage import AstroImage

try:
    from ginga.version import version
except ImportError:
    version = 'unknown'

STD_FORMAT = ('%(asctime)s | %(levelname)1.1s | '
              '%(filename)s:%(lineno)d (%(funcName)s) | %(message)s')
point_in = 1 / 72.0
point_cm = 0.0352777778


def convert(filepath, outfilepath):
    """Convert FITS image to PDF."""

    logger = logging.getLogger("example1")
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter(STD_FORMAT)
    stderrHdlr = logging.StreamHandler()
    stderrHdlr.setFormatter(fmt)
    logger.addHandler(stderrHdlr)

    fi = ImageViewCairo(logger)
    fi.configure(500, 1000)

    # Load fits file
    image = AstroImage(logger=logger)
    image.load_file(filepath)

    # Make any adjustments to the image that we want
    fi.set_bg(1.0, 1.0, 1.0)
    fi.set_image(image)
    fi.auto_levels()
    fi.zoom_fit()
    fi.center_image()

    ht_pts = 11.0 / point_in
    wd_pts = 8.5 / point_in
    off_x, off_y = 0, 0

    out_f = open(outfilepath, 'w')
    surface = cairo.PDFSurface(out_f, wd_pts, ht_pts)
    # set pixels per inch
    surface.set_fallback_resolution(300, 300)
    surface.set_device_offset(off_x, off_y)
    try:
        fi.save_image_as_surface(surface)
        surface.show_page()
        surface.flush()
        surface.finish()
    finally:
        out_f.close()


if __name__ == "__main__":
    """Run from command line."""
    usage = "usage: %prog input output"
    optprs = OptionParser(usage=usage, version=version)
    (options, args) = optprs.parse_args(sys.argv[1:])

    convert(args)

# END
