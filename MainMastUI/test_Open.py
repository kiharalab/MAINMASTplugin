import os
import Tkinter

from chimera import runCommand as rc # use 'rc' as shorthand for runCommand
from chimera import replyobj # for emitting status messages

# change to folder with data files
prevdir = os.getcwd()
newdir = prevdir + "/../MAINMAST/test3FX2"
os.chdir(newdir)

# gather the names of .pdb files in the folder
file_names = [fn for fn in os.listdir(".") if fn.endswith(".pdb")]

# loop through the files, opening, processing, and closing each in turn
for fn in file_names:
	replyobj.status("Processing " + fn) # show what file we're working on
	rc("open " + fn)
	rc("align ligand ~ligand") # put ligand in front of remainder of molecule
	rc("focus ligand") # center/zoom ligand
	rc("surf") # surface receptor
	rc("preset apply publication 1") # make everything look nice
	rc("surftransp 15") # make the surface a little bit see-through
	# save image to a file that ends in .png rather than .pdb
	png_name = fn[:-3] + "png"
	rc("copy file " + png_name + " supersample 3")
	rc("close all")
# uncommenting the line below will cause Chimera to exit when the script is done
#rc("stop now")
# note that indentation is significant in Python; the fact that
# the above command is exdented means that it is executed after
# the loop completes, whereas the indented commands that 
# preceded it are executed as part of the loop.


