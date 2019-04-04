import os
import sys
from subprocess import call
import subprocess
##import chimera

#os.chdir("..")
prevdir = os.getcwd()
newdir = prevdir + "/../MAINMAST/test3FX2"
try:
    os.chdir(newdir)
    f = open("graph.pdb", "w")
    #call(["ls", "-1"])
    subprocess.Popen(["../MAINMAST", "-m", "3FX2.situs", "-t", "9", "-filter", "0.3", "-Dkeep", "1.0", "-Ntb", "10", "-Rlocal", "5", "-Nlocal", "50", "-Nround", "50", "-Graph"], stdout=f)
except:
    print("No such file or directory")
finally:
    os.chdir(prevdir)
