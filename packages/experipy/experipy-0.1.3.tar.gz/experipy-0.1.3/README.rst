==========
 Experipy
==========

A framework for writing and running Computational Science experiments.

Experipy provides a composable grammar for automatically writing scripts and a tool which can then execute them. Support for PBS script based queueing is (mostly) implemented.

------------------
 A Simple Example
------------------

::

    from experipy.exp       import Experiment
    from experipy.grammar   import Executable

    exp = Experiment(Executable("echo", ["Hello World"]), 
                     expname="test", 
                     destdir="results")
    exp.run()

This will run the program ``echo`` with the argument ``Hello World`` in a directory in ``/tmp``, writing the output and error, along with timing information, to the directory ``results``. Directories will be created as needed. A complete example showing how to write an experiment for a Python script can be found in ``test/runtest.py``.

------------
 Components
------------

    experipy.grammar
        Contains abstractions for describing program executables, their argurments, and relationships between them such as pipelines. 

    experipy.system
        Contains a number of standard tools such as ``cp``, ``mkdir``, and the Python interpreter described as elements within the grammar.

    experipy.exp
        Contains the Experiment class, instances of which accepts a composition in the grammar, and can generate and execute a shell script from it.

    corsys
        Tools used by the Corsys research group at UTK, will likely be separated at some point, but serves as a useful example (Heavily WIP)

-----------------------
 Features In The Works
-----------------------

- Develop a means for defining configurations

- Expand ``experipy.system`` to include more standard command line tools

- Beef up PBS script options
