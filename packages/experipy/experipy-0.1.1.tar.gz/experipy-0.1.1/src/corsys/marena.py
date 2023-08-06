from os                 import path

from experipy.utils     import Namespace
from experipy.grammar   import (Executable, Wrapper, Group, 
                                GrammarViolation, tokens)

from .environment       import Env

########## Constants and helper functions ##########

Marena = Namespace("Marena",
    path = "marena",
    exe  = "marena",
    lib  = "libmarena.so",
)

def marenapath():
    return path.join(Env.projdir, Marena.path)

####################################################

class MarenaRun(Wrapper):
    def __init__(self, wrapped, hotapfile, 
                 libmarena=path.join(marenapath(), Marena.lib), 
                 opts=[], **kwargs):
        super(MarenaRun, self).__init__(
            Executable(
                path.join(marenapath(), Marena.exe),
                ["-l "+libmarena, "-f "+hotapfile] + opts + ["--", tokens.wrapped]
            ), wrapped, **kwargs
        )

