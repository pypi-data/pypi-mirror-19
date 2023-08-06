"""
    experipy.system
    ~~~~~~~~~~~~~~~

    This module provides a number of system and shell tools for helping to
    specify common tasks within the experipy grammar.
"""
from os         import path

from .grammar   import Executable

class Cd(Executable):
    def __init__(self, dirname):
        super(Cd, self).__init__("cd", [dirname])

class Cp(Executable):
    def __init__(self, target, dest, opts=[]):
        super(Cp, self).__init__("cp", opts + ['-t', dest, target])

class Mkdir(Executable):
    def __init__(self, dirname, make_parents=False):
        opts = []
        if make_parents:
            opts.append("--parents")
        super(Mkdir, self).__init__("mkdir", opts + [dirname])

class Mkfifo(Executable):
    def __init__(self, pipename):
        super(Mkfifo, self).__init__("mkfifo", [pipename])

class Rm(Executable):
    def __init__(self, *files):
        super(Rm, self).__init__("rm", ["-rf"] + list(files))

class Wait(Executable):
    def __init__(self):
        super(Wait, self).__init__("wait")

class PythonScript(Executable):
    def __init__(self, script, sopts=[], pythonexe="python", **kwargs):
        if 'inputs' in kwargs:
            kwargs['inputs'].append(path.abspath(script))
        else:
            kwargs['inputs'] = [path.abspath(script)]

        super(PythonScript, self).__init__(pythonexe, [script] + sopts, **kwargs)

class JavaApp(Executable):
    def __init__(self, jarfile, popts=[], javaexe="java", jopts=[], **kwargs):
        jarfile = path.abspath(jarfile)
        super(JavaApp, self).__init__(javaexe, jopts + ["-jar", jarfile] + popts, **kwargs)
