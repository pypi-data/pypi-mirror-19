import astrogear as pa
from .visbase import Vis


__all__ = ["VisPrint", "VisSpectrum"]


class VisPrint(Vis):
    """Prints object to screen."""

    input_classes = (object,)
    action = "Print to console"

    def _do_use(self, obj):
        print(obj)


class VisSpectrum(Vis):
    """Plots single spectrum."""

    input_classes = (pa.FileSpectrum,)
    action = "Plot spectrum"

    def _do_use(self, m):
        s = m.spectrum
        pa.plot_spectra([s])

