"""
Self-contained sub-library

  - **must not** import modules from outside this directory (self-contained)
  - should contain the most basic and general-purpose routines of the project
    (have in mind that it could make another API)
  - no project-specific hard-coded data
"""

from .conversion import *
from .debugging import *
from .fileio import *
from .introspection import *
from .loggingaux import *
from .matplotlibaux import *
from .misc import *
from .parts import *
from .search import *
from .textinterface import *
from .config import *
from .litedb import *

from . import conversion
from . import debugging
from . import fileio
from . import introspection
from . import loggingaux
from . import matplotlibaux
from . import misc
from . import parts
from . import search
from . import textinterface
from . import config
from .datetimefunc import *