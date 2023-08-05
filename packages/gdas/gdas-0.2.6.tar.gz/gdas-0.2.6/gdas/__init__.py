__version__ = '0.2.6'

import sys,os
sys.path.append(os.path.abspath(__file__).rsplit('/',1)[0]+'/ligo/')
from .epower   import *
from .plots    import *
from .retrieve import *
from .utils    import *
