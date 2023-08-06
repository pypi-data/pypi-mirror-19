"""
API to facilitate building a GUI

  - Reusable and subclassable widgets and windows
  - miscellanea of GUI-related features in `xmisc.py`
  - Python syntax highlighter
  -

File naming conventions:
  a_X*.py : classes descending from QMainWindow or QMainDialog
  a_W*.py : widgets

"""


from . import xmisc
from . import parameter
from . import syntax
# The other modules (a_*) have too ugly names to be imported

from .xmisc import *
from .parameter import *
from .syntax import *
from .errorcollector import *
from .a_WBase import *
from .a_WParametersEditor import *
from .a_WCollapsiblePanel import *
from .a_XLogDialog import *
from .a_XLogMainWindow import *
from .a_XFileMainWindow import *
from .a_XParametersEditor import *
from .a_WDBRegistry import *
from .a_WSelectFileOrDir import *
from .a_WChooseSpectrum import *
