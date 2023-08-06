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
    def __init__(self, prog, opts=None, **kwargs):
        super(Executable, self).__init__(**kwargs)
        self.prog = prog
        self.opts = []
        if opts != None:
            self.opts.extend(opts)

        if "wait" in kwargs:
            self.opts.append("&")

    def __str__(self):
        return "{0} {1}".format(self.prog, " ".join(map(str,self.opts)))


class Wrapper(ElementBase):
    def __init__(self, exe, wrapped, **kwargs):
        if not isinstance(exe, Executable):
            raise GrammarViolation("exe must be an instance of Executable")
        elif not (isinstance(wrapped, Executable) or isinstance(wrapped, Wrapper)):
            raise GrammarViolation("wrapped must be an instance of Executable or Wrapper")
        elif tokens.wrapped not in exe.opts:
            raise GrammarViolation("exe must have a '{}' option".format(tokens.wrapped))
        
        inputs = kwargs.get("inputs", [])
        if wrapped.inputs:
            inputs.extend(wrapped.inputs)
        kwargs["inputs"] = inputs

        outputs = kwargs.get("outputs", [])
        if wrapped.outputs:
            outputs.extend(wrapped.outputs)
        kwargs["outputs"] = outputs
        
        if "wait" in kwargs:
            exe.opts.append("&")

        super(Wrapper, self).__init__(**kwargs)
        self.exe = exe
        self.wrapped = wrapped

    def __str__(self):
        return str(self.exe).replace(tokens.wrapped, str(self.wrapped))


class Pipeline(ElementBase):
    def __init__(self, *parts, **kwargs):
        for part in parts:
            if not (isinstance(part, Executable) or isinstance(part, Wrapper)):
                raise GrammarViolation("'{}' is not an instance of Executable or Wrapper".format(part))
        
        inputs = kwargs.get("inputs", [])
        for part in parts:
            if part.inputs:
                inputs.extend(part.inputs)
        kwargs["inputs"] = inputs

        outputs = kwargs.get("outputs", [])
        for part in parts:
            if part.outputs:
                outputs.extend(part.outputs)
        kwargs["outputs"] = outputs
        
        super(Pipeline, self).__init__(**kwargs)
        self.parts = parts

    def __str__(self):
        return " | ".join(map(str,self.parts))


class Group(ElementBase):
    def __init__(self, *parts, **kwargs):
        for part in parts:
            if not (isinstance(part, ElementBase)):
                raise GrammarViolation("'{}' is not an instance of ElementBase".format(part))
        
        inputs = kwargs.get("inputs", [])
        for part in parts:
            if part.inputs:
                inputs.extend(part.inputs)
        kwargs["inputs"] = inputs

        outputs = kwargs.get("outputs", [])
        for part in parts:
            if part.outputs:
                outputs.extend(part.outputs)
        kwargs["outputs"] = outputs
 
        super(Group, self).__init__(**kwargs)
        self.parts = parts

    def __str__(self):
        return "\n".join(map(str,self.parts))
