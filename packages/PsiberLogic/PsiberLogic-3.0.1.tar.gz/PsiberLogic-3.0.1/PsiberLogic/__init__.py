# -*- coding: utf-8 -*-
# try statement here in case this is the first import after installation and compilation is needed
try:
    from .cPsiberLogic import *
except:
    print('PsiberLogic needs to be compiled, please call "PsiberLogic.compile()"')
from .utilities import compile, test