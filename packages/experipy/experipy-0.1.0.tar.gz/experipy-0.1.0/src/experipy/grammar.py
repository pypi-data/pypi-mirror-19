import re

from .utils import Namespace

tokens = Namespace(
    wrapped = r"[[wrapped]]",
)

class GrammarViolation(Exception):
    pass


class ElementBase(object):
    def __init__(self, **kwargs):
        self.inputs = kwargs.get("inputs", [])
        self.outputs = kwargs.get("outputs", [])


class Executable(ElementBase):
    def __init__(self, prog, opts=[], **kwargs):
        super(Executable, self).__init__(**kwargs)
        self.prog = prog
        self.opts = opts

    def __repr__(self):
        return "{0} {1}".format(self.prog, " ".join(self.opts))


class Wrapper(ElementBase):
    def __init__(self, exe, wrapped, **kwargs):
        if not isinstance(exe, Executable):
            raise GrammarViolation("exe must be an instance of Executable")
        elif not (isinstance(wrapped, Executable) or isinstance(wrapped, Wrapper)):
            raise GrammarViolation("wrapped must be an instance of Executable or Wrapper")
        elif tokens.wrapped not in exe.opts:
            raise GrammarViolation("exe must have a '{}' option".format(tokens.wrapped))
        
        super(Wrapper, self).__init__(**kwargs)
        self.exe = exe
        self.wrapped = wrapped

    def __repr__(self):
        return str(self.exe).replace(tokens.wrapped, repr(self.wrapped))


class Pipeline(ElementBase):
    def __init__(self, *parts, **kwargs):
        for part in parts:
            if not (isinstance(part, Executable) or isinstance(part, Wrapper)):
                raise GrammarViolation("'{}' is not an instance of Executable or Wrapper".format(part))
        
        super(Pipeline, self).__init__(**kwargs)
        self.parts = parts

    def __repr__(self):
        return " | ".join(map(repr,self.parts))


class Group(ElementBase):
    def __init__(self, *parts, **kwargs):
        for part in parts:
            if not (isinstance(part, ElementBase)):
                raise GrammarViolation("'{}' is not an instance of ElementBase".format(part))

        super(Group, self).__init__(**kwargs)
        self.parts = parts

    def __repr__(self):
        return "\n".join(map(repr,self.parts))
