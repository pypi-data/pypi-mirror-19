import shutil
import sys

from datetime   import datetime
from os         import chmod, makedirs, path
from subprocess import call
from time       import time

from .grammar   import ElementBase
from .system    import Cd, Cp, Mkdir, Rm
from .utils     import Namespace

Exp = Namespace("Exp",
    runsh   = "run.sh",
    shebang = "#!/bin/bash",
    rundir  = "/tmp",
    defname = "exp",
    out     = "raw.out",
    err     = "raw.err",
    timing  = "harness_time.out",
)


class ExpError(Exception):
    pass


class Experiment(object):
    def __init__(self, cmd, expname=Exp.defname, destdir=None):
        if not isinstance(cmd, ElementBase):
            raise ExpError("'{}' is not an instance of ElementBase".format(cmd))

        self.cmd     = cmd
        self.expname = expname

        if not destdir:
            self.destdir = path.abspath(expname)
        else:
            self.destdir = path.abspath(destdir)
    

    def make_runscript(self, preamble=Exp.shebang, rm_rundir=True):
        
        # Name of the temporary directory for the experiment
        rundir = path.join(Exp.rundir, self.expname + "." + str(int(time())))
        
        # Start with the preamble
        scriptstr = preamble + "\n\n"
        
        # Collect experiment input files
        scriptstr += "# Experiment setup\n"

        scriptstr += str(Mkdir(rundir, make_parents=True)) + "\n"
        scriptstr += str(Cd(rundir)) + "\n"

        for infile in self.cmd.inputs:
            scriptstr += str(Cp(path.abspath(infile), ".")) + "\n"
        
        # Execute the experiment components
        scriptstr += "\n# Run experiment\n"
        scriptstr += str(self.cmd) + "\n\n"
        
        # Exfill the experiment output files and clean up the rundir if needed
        scriptstr += "# Collect output files and clean up\n"
        for outfile in self.cmd.outputs:
            scriptstr += str(Cp(outfile, self.destdir)) + "\n"
        
        if rm_rundir:
            scriptstr += str(Rm(rundir)) + "\n"

        return scriptstr

    
    def run(self, rm_rundir=True):
        # Create the results directory, deleting any previous contents
        if path.exists(self.destdir):
            shutil.rmtree(self.destdir)
        makedirs(self.destdir)
        
        # Open the output, error and timing file handles for call
        out = open(path.join(self.destdir, Exp.out), 'w')
        err = open(path.join(self.destdir, Exp.err), 'w')
        timing = open(path.join(self.destdir, Exp.timing), 'w')

        # Write the runscript
        fname  = path.join(self.destdir, Exp.runsh)
        with open(fname, "w") as f:
            f.write(self.make_runscript(rm_rundir=rm_rundir))
        chmod(fname, 0755)

        # Execute call and time the result
        start = datetime.now()
        call(fname, stdout=out, stderr=err)
        runtime = datetime.now() - start
        timing.write(str(runtime)+"\n")

        # Clean up and close file descriptors
        out.close()
        err.close()
        timing.close()
        

    def queue(self, nodes=1, ppn=1, mem="4096m", wtime="480:00:00"):
        
        # Write the PBS script preamble
        pbsheader = (Exp.shebang
            + "\n#PBS -N {name}\n"
            + "#PBS -l nodes={nodes}:ppn={ppn},mem={mem}\n"
            + "#PBS -l walltime={wtime}\n"
            + "#PBS -o {qout}\n#PBS -e {qerr}"
            + ""
        ).format(name=self.expname, nodes=nodes, ppn=ppn, mem=mem, wtime=wtime,
            qout=path.join(self.destdir, Exp.out), 
            qerr=path.join(self.destdir, Exp.err)
        )
        
        # Create the results directory, deleting any previous contents
        if path.exists(self.destdir):
            shutil.rmtree(self.destdir)
        makedirs(self.destdir)
        
        # Write the runscript
        fname  = path.join(self.destdir, Exp.runsh)
        with open(fname, "w") as f:
            f.write(self.make_runscript(
                preamble=pbsheader, 
                rm_rundir=rm_rundir
            ))
        
        chmod(fname, 0755)
        
        # Submit to the queue
        call(["qsub", fname])
