# experipy
A framework for writing and running Computational Science experiments.

Experipy provides a composable grammar for automatically writing scripts and a tool which can then execute them. Support for PBS script based queueing is (mostly) implemented.

## A simple example

    from experipy.exp       import Experiment
    from experipy.grammar   import Executable

    exp = Experiment(Executable("echo", ["Hello World"]), 
                     expname="test", 
                     destdir="results")
    exp.run()

This will run the program `echo` with the argument `Hello World` in a directory in `/tmp`, writing the output and error, along with timing information, to the directory `results`. Directories will be created as needed. A complete example showing how to write an experiment for a Python script can be found in `test/runtest.py`.
