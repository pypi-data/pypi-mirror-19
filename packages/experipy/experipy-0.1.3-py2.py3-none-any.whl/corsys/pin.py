from os                 import path

from experipy.utils     import Namespace
from experipy.grammar   import (Executable, Wrapper, Group, 
                                GrammarViolation, tokens)

from .environment       import Env

########## Constants and helper functions ##########

Pin = Namespace("Pin",
    path = "pin-2.14",
    exe  = "pin.sh",
)

def pinpath():
    return path.join(Env.projdir, Pin.path)

####################################################

class PinTool(Wrapper):
    def __init__(self, tool, target, popts=[], topts=[], **kwargs):
        super(PinTool, self).__init__(
            Executable(
                path.join(pinpath(), Pin.exe),
                popts + ["-t "+tool] + topts + ["--", tokens.wrapped]
            ), target, **kwargs
        )

class Memtracer(PinTool):
    def __init__(self, target, popts=["-follow-execv"], topts=[], **kwargs):
        super(Memtracer, self).__init__(
            path.join(pinpath(), "source/tools/memtracer/obj-intel64/", "memtracer.so"),
            target, popts, topts, **kwargs
        )

