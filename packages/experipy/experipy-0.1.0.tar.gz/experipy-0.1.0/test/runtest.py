from os import path

from experipy.system import PythonScript
from experipy        import Experiment

if __name__ == "__main__":
    testscript = path.join(path.dirname(__file__), "test.py")
    Experiment(PythonScript(testscript, outputs=["test.out"]), 
        "test",
        path.join(path.dirname(__file__), "results/")
    ).run(rm_rundir=False)
