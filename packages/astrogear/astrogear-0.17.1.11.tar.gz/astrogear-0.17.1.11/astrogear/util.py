"""
Miscellanea routines that depend on other modules and sub-packages.

Rule: only 'gui/' modules can import util!!!
"""
from astrogear import get_default_data_path

__all__ = [
    "load_any_file", "load_spectrum", "load_spectrum_fits_messed_x", "list_data_types",
    "cut_spectrum",
]

import time
import traceback
import numpy as np
import copy
import os
import glob
import shutil
from astropy.io import fits
import astrogear as pb
from astrogear.datatypes import *




###############################################################################
# # Routines to load file of unknown format


def load_any_file(filename):
    """
    Attempts to load filename by trial-and-error using _classes as list of classes.
    """

    # Splits attempts using ((binary X text) file) criterion
    if pb.is_text_file(filename):
        return pb.load_with_classes(filename, pb.classes_txt())
    else:
        return pb.load_with_classes(filename, pb.classes_bin())


def load_spectrum(filename):
    """
    Attempts to load spectrum as one of the supported types. Returns a Spectrum, or None
    """
    f = pb.load_with_classes(filename, pb.classes_sp())
    if f:
        return f.spectrum
    return None


def load_spectrum_fits_messed_x(filename, sp_ref=None):
    """Loads FITS file spectrum that does not have the proper headers. Returns a Spectrum"""

    # First tries to load as usual
    f = pb.load_with_classes(filename, (FileSpectrumFits,))

    if f is not None:
        ret = f.spectrum
    else:
        hdul = fits.open(filename)

        hdu = hdul[0]
        if not hdu.header.get("CDELT1"):
            hdu.header["CDELT1"] = 1 if sp_ref is None else sp_ref.delta_lambda
        if not hdu.header.get("CRVAL1"):
            hdu.header["CRVAL1"] = 0 if sp_ref is None else sp_ref.x[0]

        ret = Spectrum()
        ret.from_hdu(hdu)
        ret.filename = filename
        original_shape = ret.y.shape  # Shape of data before squeeze
        # Squeezes to make data of shape e.g. (1, 1, 122) into (122,)
        ret.y = ret.y.squeeze()

        if len(ret.y.shape) > 1:
            raise RuntimeError(
                "Data contains more than 1 dimension (shape is {0!s}), FITS file is not single spectrum".format(
                original_shape))

    return ret


def list_data_types():
    """Prints a list with all data types, in Markdown table format"""
    ll = []  # [(description, default filename), ...]


    for item in dir(pb.classes_file()):
        attr = pb.datatypes.__getattribute__(item)

        doc = attr.__doc__
        doc = attr.__name__ if doc is None else doc.strip().split("\n")[0]

        def_ = attr.default_filename
        def_ = def_ if def_ is not None else "-"
        ll.append((doc, def_))

    ll.sort(key=lambda x: x[0])

    return pb.markdown_table(("File type", "Default filename (for all purposes)"), ll)


def cut_spectrum(sp, l0, lf):
    """
    Cuts spectrum given a wavelength interval

    Arguments:
        sp -- Spectrum instance
        l0 -- initial wavelength
        lf -- final wavelength
    """

    if l0 >= lf:
        raise ValueError("l0 must be lower than lf")
    idx0 = np.argmin(np.abs(sp.x - l0))
    idx1 = np.argmin(np.abs(sp.x - lf))
    out = copy.deepcopy(sp)
    out.x = out.x[idx0:idx1]
    out.y = out.y[idx0:idx1]
    return out


def copy_default_data_file(filename, module=pb):
    """Copies file from pyfant/data/default directory to local directory."""
    fullpath = get_default_data_path(filename, module=module)
    shutil.copy(fullpath, ".")