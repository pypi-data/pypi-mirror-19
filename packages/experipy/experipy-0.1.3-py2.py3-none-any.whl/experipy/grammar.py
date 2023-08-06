"""
    experipy.grammar
    ~~~~~~~~~~~~~~~~

    This module provides the core elements which compose the Experipy grammar:
    Executables, Wrappers, Pipelines, and Groups. These elements facilitate 
    specifying programs to execute as well as the files they depend on. 
"""
import re

from .utils import Namespace

tokens = Namespace(
    wrapped = r"[[wrapped]]",
)

class GrammarViolation(Exception):
    pass


class Element(object):
    """The Element class forms the grammar's base class.

    Parameters
    ----------
    inputs : list
        A list of strings which are the names of files that the Element relies
        on for input. These will be copied to the run directory when an 
        Experiment is used to run the Element.
    outputs: list
        A list of strings which are the names of files that the Element is 
        expected to generate as output. These will be copied from the run
        directory when an Experiment is used to run the Element.
    """

    def __init__(self, **kwargs):
        self.inputs = kwargs.get("inputs", [])
        self.outputs = kwargs.get("outputs", [])


class Executable(Element):
    """Executable objects should represent a single program and its arguments.

    Parameters
    ----------
    prog : str
        The name of the program executable.
    opts : list
        A list of command line options to pass to the program. Defaults to
        an empty list if not provided.
    wait : bool
        If False, a '&' will be appended to the argument list, indicating to
        the shell that it should background the program instead of blocking
        on it. Defaults to True.
    """

    def __init__(self, prog, opts=None, wait=True, **kwargs):
        super(Executable, self).__init__(**kwargs)
        self.prog = prog
        self.opts = []
        if opts != None:
            self.opts.extend(opts)

        if wait == False:
            self.opts.append("&")

    def __str__(self):
        """Render the Executable as it will appear in the shell script."""
        return "{0} {1}".format(self.prog, " ".join(map(str,self.opts)))


class Wrapper(Element):
    """Wrapper objects allow one program to wrap another.

    Provides a way to specify programs such as GDB or Valgrind, which wrap
    around another program to alter or observe its execution.

    Parameters
    ----------
    exe : experipy.Executable
        The wrapping Executable. Must provide a '[[wrapped]]' option which 
        indicates where the wrapped Element should be placed when rendering
        the script.
    wrapped : experipy.Executable or experipy.Wrapper
        The wrapped Executable or Wrapper. Inputs and outputs specified to 
        exe and wrapped will also be included in the resultant object's inputs 
        and outputs.
    wait : bool
        If False, a '&' will be appended to the argument list, indicating to
        the shell that it should background the program instead of blocking on
        it. Defaults to True.

    """

    def __init__(self, exe, wrapped, wait=True, **kwargs):
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
        
        if wait == False:
            exe.opts.append("&")

        super(Wrapper, self).__init__(**kwargs)
        self.exe = exe
        self.wrapped = wrapped

    def __str__(self):
        """Render the Wrapper as it will appear in the shell script."""
        return str(self.exe).replace(tokens.wrapped, str(self.wrapped))


class Pipeline(Element):
    """Pipeline objects allow specification of pipelined workflows.

    A Pipeline takes one or more Element parts, and joins them with a '|'
    operator, indicating to the shell that each part should recieve its input
    from the previous part, and provide its output to the next.

    Parameters
    ----------
    *parts : 
        One or more Executables or Wrappers to be chained together into a 
        pipeline. Inputs and outputs to the individual parts will be included
        in the Pipeline's inputs and outputs.
    """

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
        """Render the Pipeline as it will appear in the shell script."""
        return " | ".join(map(str,self.parts))


class Group(Element):
    """Group objects allow specification of Executables to be run in order.

    In the resultant script, a Group's parts will be included one after another,
    in the order they were specified. Groups should be used when specifying 
    complex experiments involving multiple steps like set up or post-processing,
    or combined with the wait parameter to Executable to specify programs which
    should be run concurrently.

    Parameters
    ----------
    *parts :
        One or more Elements to be placed into the script. Inputs and outputs
        to the individual parts will be included in the Group's inputs and 
        outputs.
    """
    def __init__(self, *parts, **kwargs):
        for part in parts:
            if not (isinstance(part, Element)):
                raise GrammarViolation("'{}' is not an instance of Element".format(part))
        
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
        """Render the Group as it will appear in the shell script."""
        return "\n".join(map(str,self.parts))
