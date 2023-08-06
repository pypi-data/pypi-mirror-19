# # Temporary imports
#   =================
# These modules should be be del'eted at the end
import sys
from PyQt4.QtGui import QFont
import logging

# # Prevents from running in Python 2
#   =================================
# (http://stackoverflow.com/questions/9079036)
if sys.version_info[0] < 3:
    raise RuntimeError("Python version detected:\n*****\n{0!s}\n*****\nCannot run, must be using Python 3".format(sys.version))


# # Initializes matplotlib to work with Qt4
#   =======================================
# Tk backend problems:
# - plot windows pop as modal
# - configuration options not as rich as Qt4Agg
# However, if another backend has been chosen before importing astroapi, will not choose Qt4 backend
def init_agg():
    import matplotlib
    matplotlib.use('Qt4Agg')
if not 'matplotlib.backends' in sys.modules:
    init_agg()



# # Setup
#   =====

# ## Constants affecting the Graphical User Interface style
#    ------------------------------------------------------

# ### Color definition
# Error color
COLOR_ERROR = "#AA0000" # sortta wine
# Warning color
COLOR_WARNING = "#C98A00" # sortta yellow
# Default color for label text
COLOR_DESCR = "#222222"

# ### Standard font to be used in all GUIs
MONO_FONT = QFont("not_a_font_name")
MONO_FONT.setStyleHint(QFont.TypeWriter)


# ## Constants affecting logging
#    ---------------------------
#
# If the following need change, this should be done before calling get_python_logger() for the
# first time

# Set this to make the python logger to log to the console. Note: will have no
# effect if changed after the first call to get_python_logger()
flag_log_console = True

# Set this to make the python logger to log to a file named "python.log".
# Note: will have no effect if changed after the first call to get_python_logger()
flag_log_file = False

# Logging level for the python logger
logging_level = logging.INFO



# # Imports
#   =======
# **Note** The import order is roughly the module dependency order
from .gear import *
from .datatypes import *
from .vis import *
from .paths import *
from .util import *
from .xgear import *
from .collaborate import *
from .gui import *
from .physics import *
from . import datatypes
from . import vis
from . import xgear



# # Function to access package-specific config file
#   ===============================================
def get_config():
    """Returns AAConfigObj object that corresponds to file ~/.astrogear.conf"""
    return get_config_obj(".astrogear.conf")



# # Finally, gets rid of unwanted symbols in the workspace
#   ======================================================
del QFont, init_agg, sys, logging  # Don't want this in the namespace

#
#
#
