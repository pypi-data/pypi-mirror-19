from os import getenv
from experipy.utils import Namespace

projectdir = getenv("CORSYS_PROJDIR", "")
if not projectdir:
    projectdir = raw_input("CORSYS_PROJDIR not set, provide the project directory path\n>>> ")

resultdir = getenv("CORSYS_RESDIR", "")
if not resultdir:
    resultdir = raw_input("CORSYS_RESDIR not set, provide the result directory path\n>>> ")

Env = Namespace(
    projdir = projectdir,
    resdir  = resultdir,
)
