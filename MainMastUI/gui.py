#    Import the standard modules.
import os
from Tkinter import *
import ttk 
import Tkinter, tkFileDialog
import tkMessageBox
import sys
from subprocess import call
import subprocess
import time
from threading import Thread
from shutil import copyfile
import datetime
from distutils.dir_util import copy_tree
from sys import platform


#    Import the Chimera modules and classes.
import chimera
from chimera.baseDialog import ModelessDialog
from chimera.misc import getPseudoBondGroup
from chimera import runCommand as rc # use 'rc' as shorthand for runCommand
from chimera import replyobj # for emitting status messages

#    Import the package for which the graphical user interface
#    is designed.
import MainMastUI

#    Import the file we used to store the working path
#    The file is named 'WorkPath.py'.
import WorkPath

#
#    Here we declare a MainchainDialog class that derives from ModelessDialog and
#    customize it for the specific needs of this MAINMAST extension.
class MainchainDialog(ModelessDialog):

    # import all the variables we need in this plugin
    name = "MAINMAST ui"
    global workingPath
    workingPath = "working path"
    global fileNameLabel
    fileNameLabel = {}

    # declare corresponding variables used in MAINMAST command
    # t: Threshold of density values,
    # Pfilter: Filter of representative points,
    # Dkeep: Keep edge where distance < [f],
    # Ntb: Size of tabu-list, def = 100,
    # Rlocal: Radius of Local MST, def = 10,
    # Nround: Number of Iterations, def = 5000.
    global t
    global Pfilter
    global Dkeep
    global Ntb
    global Rlocal
    global Nround
    global MCP_Num
    global CA_Num
    global filePath
    global fileName
    global outfilePath
    global MSTcreate
    global AEcreate
    global Pathcreate
    global CAcreate
    global MSTAE
    global compMASTAE
    global fileCount
    global recreate
    global pnixW
    global mapOpen
    global saveHistoryPopUp
    global compareHistoryPopUp
    global checkValuePopup
    global history_name
    global select1
    global select2
    global select3
    global spd3filePathPrev
    global storeFilePopUp
    global select_file1_Name
    global select_file2_Name
    global select_file3_Name
    global MSTcreated_check
    global CAcreated_check
    global currentFileStored
    global restored_from_file
    global MSTcreate

    t=1
    Pfilter=0.3
    Dkeep=1.0
    Ntb=10
    Rlocal=5
    Nround=50
    MCP_Num = 1
    CA_Num = 1
    MSTAE = 0
    compMASTAE = 0
    fileCount = 0
    recreate = 0
    pnixW = "Default"
    # mapFile = 0
    # curMap = 0
    # mapFir = 0
    fileName = "unknown"
    outfilePath = "undefined"
    filePath = "undefined"
    mapOpen = 0
    currentFileStored = 0
    restored_from_file = 0
    #fileName = "1yfq"
    #prevdir = os.getcwd()
    #newdir = prevdir + "/chimera/MAINMAST/" + fileName
    #try:
    #    os.chdir(newdir)
    #    fn=fileName+".pdb"
    #    model=chimera.openModels.open(fn)
#            except:
#                print("No such file or directory")
    #finally:
    #    os.chdir(prevdir)



    #    The buttons displayed at the bottom of the dialog are given
    #    in the class variable 'buttons'.  For modeless dialogs, a
    #    help button will automatically be added to the button list
    #    (the help button will be grayed out if no help information
    #    is provided).  For buttons other than 'Help', clicking on
    #    them will invoke a class method of the same name. Here we 
    #    define a "Set Working Path" botton which will pop up the 
    #    working path setup window.
    #
    #    Both dialog base classes provide appropriate methods for
    #    'Close', so we won't provide a 'Close' method in this
    #    subclass.  The ModelessDialog base class also provides a
    #    stub method for 'Apply', but we will override it with our
    #    own 'Apply' method later in the class definition.
    buttons = ("Close")

    #    A help file or URL can be specified with the 'help' class
    #    variable.  A URL would be specified as a string (typically
    #    starting with "http://...").  A file would be specified as
    #    a 2-tuple of file name followed by a package.  The file
    #    would then be looked for in the 'helpdir' subdirectory of
    #    the package.  A dialog of Chimera itself (rather than of an
    #    imported package) might only give a filename as the class
    #    help variable.  That file would be looked for in
    #    /usr/local/chimera/share/chimera/helpdir.

    #    The title displayed in the dialog window's title bar is set
    #    via the class variable 'title'.
    title = "MAINMAST"


    
    


    #    Here we define the function called after click "Set Working Path" botton
    #    A popup window appears asking the user to change the working Path to
    #    where the MAINMAST file is stored at. This set up need only to do once.

    def SetWorkingPath(self):
        global workingPath
        global workPathEntry
        print(workingPath)

        #   This defines the function after clicking the "select" botton.
        #   It will pop up a dialog to select working directory.
        def select_working_path_Callback():
            global workingPath
            
            workPathEntry.delete(0, "end")
            workingPath=tkFileDialog.askdirectory()
            workPathEntry.insert(0, workingPath)

        #   This defines the function after clicking the "change" botton.
        #   It will change the working path stored in WorkPath.py
        #   After change the address, all path in this program will update.
        def change_working_path_Callback():
            global workingPath

            workingPath=workPathEntry.get()
            workPathDir = workingPath + "/WorkPath.py"
            f= open(workPathDir,"w+")
            writePath = "def showWorkingPath():\n    return \"" + workingPath +"\""
            f.write(writePath)
            workingPath = WorkPath.showWorkingPath()


        #   The following part defines the layout of Change Working Path Popup.
        workPathPopUp = Toplevel()
        label1 = Label(workPathPopUp, text="Current Working Directory:", height=2)
        label1.grid(row=1,column=1, columnspan=2, sticky=Tkinter.W)

        workPathEntry = Tkinter.Entry(workPathPopUp, width=50)
        prevdir = os.getcwd()
        print(prevdir)
        workingPath = WorkPath.showWorkingPath()
        workPathEntry.insert(0, workingPath)
        workPathEntry.grid(row=2, column=1, columnspan=2)

        selectPath_Button = Tkinter.Button(workPathPopUp, text="select", width=20, height=1, command=select_working_path_Callback)
        selectPath_Button.grid(row=4,column=1, columnspan=2, sticky=Tkinter.W)

        changePath_Button = Tkinter.Button(workPathPopUp, text="change", width=20, height=1, command=change_working_path_Callback)
        changePath_Button.grid(row=4,column=2, columnspan=2, sticky=Tkinter.E)

        workingPath = WorkPath.showWorkingPath()



    #    Both ModelessDialog and ModalDialog, in their __init__
    #    functions, set up the standard parts of the dialog interface
    #    (top-level window, bottom-row buttons, etc.) and then call
    #    a function named 'fillInUI' so that the subclass can fill
    #    in the parts of the interface specific to the dialog.  As
    #    an argument to the function, a Tkinter Frame is provided
    #    that should be the parent to the subclass-provided interface
    #    elements.
    def fillInUI(self, parent):

        #   Check the working directory everytime the program starts.
        #   User will know if they have the working path setup correct.
        currentDir = os.getcwd()
        print(currentDir)
        global MSTcreate
        global CAcreate


        #   This def is used for error checking. To check if the input
        #   varibles for the MainMast is number. It returns a boolean 
        #   after the checking.
        def is_number(s):
            try:
                float(s)
                return True
            except ValueError:
                return False


        #   This method takes all the variable needed for MainMast command
        #   and generate MainMast Output files.
        #   Explaination of parameters:
        #   filePath: the Directory where the input file is located at
        #   fileNamePrev: the input of the 
        #   t: Threshold of density values,
        #   Pfilter: Filter of representative points,
        #   Dkeep: Keep edge where distance < [f],
        #   Ntb: Size of tabu-list, def = 100,
        #   Rlocal: Radius of Local MST, def = 10,
        #   Nround: Number of Iterations, def = 5000.
        #   ifPath: a identifier indicating if we are creating all files or not.

        def create_file(filePath,fileNamePrev,t,Pfilter,Dkeep,Ntb,Rlocal,Nround,ifPath):

            #   this global variable indicates if the user has used the
            #   compare history function. If so, the program will close
            #   the compare history graph and display regular graph.
            global recreate

            #   file name is refer to the input file name.
            global fileName
            global restored_from_file
            global currentFileStored


            #   Those steps is used to verify if the MainMast file folder
            #   already exists. If not, it will create a new one.
            outfilePath = WorkPath.showWorkingPath()
            print(outfilePath)
            end = outfilePath.find('/MainMastUI')
            outfilePath = outfilePath[0:int(end)]
            prevdir = os.getcwd()
            restored_from_file = 0
            currentFileStored = 0
            try:
                os.chdir(outfilePath)

                if not os.path.exists("MAINMAST/MAINMASTfile"):
                    os.makedirs("MAINMAST/MAINMASTfile")
                else:

                    filelist = [ file for file in os.listdir(outfilePath + "/MAINMAST/MAINMASTfile") ]
                    for f in filelist:
                        os.remove(os.path.join(outfilePath + "/MAINMAST/MAINMASTfile", f))
            except:
                tkMessageBox.showwarning("Error", "Something went wrong, please check WorkPath.py")
                os.chdir(prevdir)
                return
            finally:
                os.chdir(prevdir)


            #   The program set the current working directory to
            #   where the MAINMASTfile folder is located at, and
            #   start to create MainMast output files in this folder.
            newdir = outfilePath + "/MAINMAST/MAINMASTfile"
            fileName = fileNamePrev.split(".")[0]


            #   The follow part check if the input file is in '.pdb' 
            #   or '.mrc' format. If so, then it will generate a ".situs"
            #   file for use.
            if (fileNamePrev.split(".")[1] == 'pdb'):
                outputFile = fileName + ".mrc"
                inputFile = fileName + ".pdb"
                i = subprocess.Popen(["e2pdb2mrc.py", inputFile, outputFile], stdout=subprocess.PIPE)
                print i.communicate()

                outputFile = fileName + ".situs"
                inputFile = fileName + ".mrc"
                sC = subprocess.Popen(('echo', '2'), stdout=subprocess.PIPE)
                output = subprocess.check_output(('map2map', inputFile, outputFile), stdin=sC.stdout)
                sC.wait()
                print sC.communicate()

            if (fileNamePrev.split(".")[1] == 'mrc'):
                outputFile = fileName + ".situs"
                inputFile = fileName + ".mrc"
                sC = subprocess.Popen(('echo', '2'), stdout=subprocess.PIPE)
                output = subprocess.check_output(('map2map', inputFile, outputFile), stdin=sC.stdout)
                sC.wait()
                print sC.communicate()


            #   copy the file we need to MIANMASTfile folder for 
            #   MainMast program to excute. "current.situs" is used
            #   for display the density map.
            situsFile = fileName + ".situs"
            situsPath = newdir + "/" + situsFile
            currentSitus = "current.situs"
            currentSitusPath = newdir + "/" + currentSitus
            subprocess.Popen(["cp", filePath, situsPath])
            subprocess.Popen(["cp", filePath, currentSitusPath])

            seqFile = fileName + ".seq"
            spd3File_name = fileName + ".spd3"
            spd3File = "current.spd3"
            pssmFile = fileName + ".pssm"

            try:
                copyfile(spd3fileName.get(), newdir + "/" + spd3File)
                copyfile(spd3fileName.get(), newdir + "/" + spd3File_name)
            except:
                print(".spd3 file Does not exist")

            

            #   remove old files in that folder. If the MainMast
            #   output file is already exists in the folder, we 
            #   have to delete them so that we can generate new files.
            try:
                oldGraph = newdir + "/graph.pdb"
                oldTree = newdir + "/tree.pdb"
                oldPath = newdir + "/path.pdb"
                oldCA = newdir + "/CA.pdb"
                oldCA_r = newdir + "/CA_r.pdb"
                os.remove(oldGraph)
                os.remove(oldTree)
                os.remove(oldPath)
                os.remove(oldCA)
                os.remove(oldCA_r)
                print("removed old files and ready to create pdb files")
            except:
                print("ready to create pdb files")


            #   the following are the excution of MAINMAST command.
            #   Used python Popen method.
            try:
                os.chdir(newdir)
                global MSTcreate
                global AEcreate
                global Pathcreate

                if ifPath:
                    f = open("path.pdb", "w")
                    # p = subprocess.Popen(["../MAINMAST", "-m", situsFile, "-t", t, "-filter", Pfilter, "-Dkeep", Dkeep, "-Ntb", Ntb, "-Rlocal", Rlocal, "-Nlocal", "50", "-Nround", Nround, "-Path"], stdout=f)
                    p = subprocess.Popen(["../MAINMAST", "-m", currentSitusPath, "-t", t, "-filter", Pfilter, "-Dkeep", Dkeep, "-Ntb", Ntb, "-Rlocal", Rlocal, "-Nlocal", "50", "-Nround", Nround, "-Path"], stdout=f)
                    p.communicate()
                    # This part left here if want to indicate 'Path.pdb' creation process
                    # Pathcreate = Tkinter.Label(parent, text="Path.pdb:                    ")
                    # Pathcreate.grid(row=14, column=2, columnspan=2, sticky=Tkinter.W)
                    # Pathcreate = Tkinter.Label(parent, text="Path.pdb:  ready to display")
                    # Pathcreate.grid(row=14, column=2, columnspan=2, sticky=Tkinter.W)
                    f.close()

                f = open("graph.pdb", "w")          
                g = subprocess.Popen(["../MAINMAST", "-m", currentSitusPath, "-t", t, "-filter", Pfilter, "-Dkeep", Dkeep, "-Ntb", Ntb, "-Rlocal", Rlocal, "-Nlocal", "50", "-Nround", Nround, "-Graph"], stdout=f)
                
                g.communicate()
                f.close()
                # This part left here if want to indicate 'Graph.pdb' creation process
                # AEcreate = Tkinter.Label(parent, text="All Edges:                    ")
                # AEcreate.grid(row=11, column=2, columnspan=2, sticky=Tkinter.W)
                # AEcreate = Tkinter.Label(parent, text="All Edges:  ready to display")
                # AEcreate.grid(row=11, column=2, columnspan=2, sticky=Tkinter.W)

                

                f = open("tree.pdb", "w")
                t = subprocess.Popen(["../MAINMAST", "-m", currentSitusPath, "-t", t, "-filter", Pfilter, "-Dkeep", Dkeep, "-Ntb", Ntb, "-Rlocal", Rlocal, "-Nlocal", "50", "-Nround", Nround, "-Tree"], stdout=f)
                t.communicate()
                f.close()

                #   This updates "MST & all Edges:  file not created" to
                #   "MST & all Edges:  ready to display". So the following
                #   code changes the UI.
                MSTcreate = Tkinter.Label(createFileUI.sub_frame, text="MST & all Edges:                    ")
                MSTcreate.grid(row=13, column=0, columnspan=2, sticky=Tkinter.W)
                MSTcreate = Tkinter.Label(createFileUI.sub_frame, text="MST & all Edges: ready to display")
                MSTcreate.grid(row=13, column=0, columnspan=2, sticky=Tkinter.W)

            except:
                tkMessageBox.showwarning("Error", "Something went wrong when generating files, please try again")
                os.chdir(prevdir)
                return
            #   After "Path.pdb", "Graph.pdb" and "Tree.pdb" created, python
            #   respondes with "all files created"
            finally:
                print("all files created")
                os.chdir(prevdir)
                recreate = 1


        #   define the text showing on the left column bottons
        MSTree = 'Minimum Spanning Tree'
        AllEdges = 'All         Edges'
        MCPath = 'Main-chain Path'
        CAModel = 'Predicted CA model'
        pulchra = 'Pulchra        Rebuild'
        ModelPanel = 'Model Panel'

        def check_MST_created():
            # global MSTcreate
            # global CAcreate
            global MSTcreated_check
            MSTcreated = MSTcreate.cget("text")
            if "ready to display" not in MSTcreated:
                tkMessageBox.showwarning("Warning","Please create file first\n\nOr restore your saved file in 'Save and Restore files'")
                MSTcreated_check = 0
            else:
                MSTcreated_check = 1

        def check_CA_created():
            # global MSTcreate
            # global CAcreate
            global CAcreated_check
            CAcreated = CAcreate.cget("text")
            if "ready to display" not in CAcreated:
                tkMessageBox.showwarning("Warning","Please create file first\n\nOr restore your saved file in 'Save and Restore files'")
                CAcreated_check = 0
            else:
                CAcreated_check = 1


        #   his callback will be called after the user click left column
        #   "Minimum Spanning Tree" or "All Edges" botton at the first time.
        #   This function opens 'tree.pdb' and 'graph.pdb', create bonds
        #   according to the file, and then hide those two graphs for future use.
        def MSTAE_callback():
            outfilePath = WorkPath.showWorkingPath()
            end = outfilePath.find('/MainMastUI')
            outfilePath = outfilePath[0:int(end)]
            prevdir = os.getcwd()
            newdir = outfilePath + "/MAINMAST/MAINMASTfile"

            try:
                os.chdir(newdir)

                #   the following steps generates the graph for "tree.pdb"
                fn = "tree.pdb"
                rc("close all")
                modelMST=chimera.openModels.open(fn)

                try:
                    res=modelMST[0].residues
                except:
                    print("file not ready yet")

                rc("~bond")
                rc("display #0")
                with open("tree.pdb") as pdbfile:
                    grp=getPseudoBondGroup("MST", associateWith=modelMST)
                    for line in pdbfile:
                        if line[:4] == 'BOND':
                            grp.newPseudoBond(res[int(line[7:11])-1].atomsMap['CA'][0], res[int(line[13:17])-1].atomsMap['CA'][0])



                #   the following steps generates the graph for "tree.pdb"
                fn = "graph.pdb"
                modelAE=chimera.openModels.open(fn)
                try:
                    res=modelAE[0].residues
                except:
                    print("file not ready yet")
                rc("~bond")
                rc("display #1")
                with open("graph.pdb") as pdbfile:
                    grp=getPseudoBondGroup("AE", associateWith=modelAE)
                    for line in pdbfile:
                        if line[:4] == 'BOND':
                            grp.newPseudoBond(res[int(line[7:11])-1].atomsMap['CA'][0], res[int(line[13:17])-1].atomsMap['CA'][0])
                

                #   Change the display settings and hide "tree.pdb" and "graph.pdb"
                rc("repr bs")
                rc("vdwdefine 1")
                rc("~modeldisp #0")
                rc("~modeldisp #1")
            except (IOError),e:
                    tkMessageBox.showwarning("Error", "File Error")
            finally:
                os.chdir(prevdir)


        #   This callback is called when the user click "Minimum Spanning Tree" botton.
        #   This callback shows the MST and remain the direction of previous graphs.
        def MST_callback():
            global MSTAE
            global compMASTAE
            global fileCount
            global recreate
            global MSTcreated_check

            check_MST_created()

            if MSTcreated_check:
                if recreate:
                    MSTAE = 0
                    rc("close all")
                    recreate = 0
                if not MSTAE or compMASTAE:
                    MSTAE_callback()
                    MSTAE = 1
                    compMASTAE = 0
                if fileCount != 0:
                    for i in range (2, fileCount + 2):
                        rc("close #" + `i`)
                rc("modeldisp #0")
                rc("~modeldisp #1")
                rc("repr bs")
                rc("vdwdefine 1")
                rc("setattr g lineWidth 2")
                rc("setattr p color black")
                rc("setattr m ballScale 0.35")



        #   This callback is called when the user click "All Edges" botton.
        #   This callback shows the MST and remain the direction of previous graphs.
        def AE_callback():
            global MSTAE
            global compMASTAE
            global fileCount
            global recreate
            global MSTcreated_check

            check_MST_created()

            if MSTcreated_check:
                if recreate:
                    MSTAE = 0
                    rc("close all")
                    recreate = 0
                if not MSTAE or compMASTAE:
                    MSTAE_callback()
                    MSTAE = 1
                    compMASTAE = 0
                if fileCount != 0:
                    for i in range (2, fileCount + 2):
                        rc("close #" + `i`)
                rc("modeldisp #1")
                rc("~modeldisp #0")
                rc("repr bs")
                rc("vdwdefine 1")
                rc("setattr g lineWidth 2")
                rc("setattr p color black")
                rc("setattr m ballScale 0.35")



        #   This callback is called when the user click "Model Panel" botton.
        def ModelPanel_callback():
            rc("start Model Panel")


        #   This callback is called when the user click "Main Chain Path" botton.
        def MCP_callback():
            global MCP_Num
            global CA_Num
            global MSTAE
            global compMASTAE
            global fileCount
            global CAcreated_check

            check_CA_created()

            if not CAcreated_check:
                return


            MCP_Num=MCP_Variable.get()
            CA_Num=CA_Variable.get()
            outfilePath = WorkPath.showWorkingPath()
            end = outfilePath.find('/MainMastUI')
            outfilePath = outfilePath[0:int(end)]
            prevdir = os.getcwd()
            newdir = outfilePath + "/MAINMAST/MAINMASTfile"


            #   if the user has not generated the Minimum Spanning tree and All
            #   Edges, it will generate those two graphs first and then hide them.
            try:
                if not MSTAE or compMASTAE:
                    MSTAE_callback()
                    MSTAE = 1
                    compMASTAE = 0
                else:
                    if fileCount != 0:
                        for i in range (2, fileCount + 2):
                            rc("close #" + `i`)

                rc("~modeldisp #0")
                rc("~modeldisp #1")

                os.chdir(newdir)


                #   in order for the Main Chain path to look better, we display
                #   the CA graph first.
                fn = "CA.pdb"
                try:
                    modelAE=chimera.openModels.open(fn)
                except (IOError),e:
                    tkMessageBox.showwarning("Error", "CA File not read properly")
                    os.chdir(prevdir)
                    return
                rc("~bond")
                rc("display")
                rc("repr bs")
                rc("vdwdefine 2")
            finally:
                os.chdir(prevdir)


            #   display the Main Chain Paths based on how many graphs the user
            #   wants to see.
            outfilePath = WorkPath.showWorkingPath()
            outfilePath = outfilePath[0:int(end)]
            prevdir = os.getcwd()
            newdir = outfilePath + "/MAINMAST/MAINMASTfile"
            try:
                os.chdir(newdir)

                for i in range (0, int(MCP_Num)):
                    fn = "path" + `i` + ".pdb"
                    modelMCP=chimera.openModels.open(fn)
                    rc("matrixcopy #0 #" + `i`) 
                fileCount = int(MCP_Num) + 1
            finally:
                os.chdir(prevdir)


        #   This callback is called when the user click the "Predicted CA model"
        #   botton. It displays the optimal CA model and display other CA models
        #   based on the users chioce.
        def CA_callback():
            global MCP_Num
            global CA_Num
            global MSTAE
            global compMASTAE
            global fileCount
            global CAcreated_check

            check_CA_created()

            if not CAcreated_check:
                return

            MCP_Num=MCP_Variable.get()
            CA_Num=CA_Variable.get()
            outfilePath = WorkPath.showWorkingPath()
            end = outfilePath.find('/MainMastUI')
            outfilePath = outfilePath[0:int(end)]
            prevdir = os.getcwd()
            newdir = outfilePath + "/MAINMAST/MAINMASTfile"

            try:
                if not MSTAE or compMASTAE:
                    MSTAE_callback()
                    MSTAE = 1
                    compMASTAE = 0
                else:
                    if fileCount != 0:
                        for i in range (2, fileCount + 2):
                            rc("close #" + `i`)

                rc("~modeldisp #0")
                rc("~modeldisp #1")

                os.chdir(newdir)
                fn = "CA.pdb"
                try:
                    modelCA=chimera.openModels.open(fn)
                except (IOError),e:
                    tkMessageBox.showwarning("Error", "CA File not read properly")
                    os.chdir(prevdir)
                    return

                rc("~bond")
                rc("display")
                rc("repr bs")
                rc("vdwdefine 2")

                try:
                    res=modelCA[0].residues
                

                    grp=getPseudoBondGroup("CA", associateWith=modelCA)
                    for i in range (0, len(res) - 2):
                        grp.newPseudoBond(res[i].atomsMap['CA'][0], res[i+1].atomsMap['CA'][0])


                    rc("setattr g lineWidth 3")
                    rc("setattr p color black")
                except:
                    print("file not ready yet")
            finally:
                os.chdir(prevdir)

            outfilePath = WorkPath.showWorkingPath()
            end = outfilePath.find('/MainMastUI')
            outfilePath = outfilePath[0:int(end)]
            prevdir = os.getcwd()
            newdir = outfilePath + "/MAINMAST/MAINMASTfile"
            seqFile = fileName + ".seq"
            spd3File = fileName + ".spd3"
            try:
                os.chdir(newdir)
                
                for i in range (0, int(CA_Num)):
                    fn = "CA" + `i` + ".pdb"
                    modelAE=chimera.openModels.open(fn)
                    rc("matrixcopy #0 #" + `i`) 
                fileCount = int(CA_Num) + 1
            finally:
                os.chdir(prevdir)


        #   This callback is called when the user click the "Pulchra Rebuild"
        #   botton. It displays the pulchar model. However, in order for this
        #   function to work, the system should have pulchra preinstalled.
        def pulchra_callback():
            global MSTAE
            global fileCount
            outfilePath = WorkPath.showWorkingPath()
            end = outfilePath.find('/MainMastUI')
            outfilePath = outfilePath[0:int(end)]
            prevdir = os.getcwd()
            newdir = outfilePath + "/MAINMAST/MAINMASTfile"
            global CAcreated_check

            check_CA_created()

            if not CAcreated_check:
                return

            #   if the user clicked the pulchar before view MST and AE,
            #   the program will first generate MST and AE and then hide
            #   those two graphs.
            try:
                if not MSTAE:
                    MSTAE_callback()
                    MSTAE = 1
                else:
                    if fileCount != 0:
                        for i in range (2, fileCount + 2):
                            rc("close #" + `i`)

                rc("~modeldisp #0")
                rc("~modeldisp #1")


                #   The program will show the Pulchar result graph with 
                #   CA model graph. So the program will first display 
                #   the CA model graph.
                os.chdir(newdir)
                fn = "CA.pdb"
                try:
                    modelCA=chimera.openModels.open(fn)
                except (IOError),e:
                    tkMessageBox.showwarning("Error", "CA File not read properly")
                    os.chdir(prevdir)
                    return

                rc("~bond")
                rc("display")
                rc("repr bs")
                rc("vdwdefine 2")

                try:
                    res=modelCA[0].residues
                    grp=getPseudoBondGroup("CA", associateWith=modelCA)
                    for i in range (0, len(res) - 2):
                        grp.newPseudoBond(res[i].atomsMap['CA'][0], res[i+1].atomsMap['CA'][0])
                    rc("setattr g lineWidth 3")
                    rc("setattr p color black")


                except:
                    print("file not ready yet")

                
                fn = "CA.rebuilt.pdb"
                try:
                    modelCArebuilt=chimera.openModels.open(fn)
                except (IOError),e:
                    tkMessageBox.showwarning("Error", "CA File not read properly")
                    os.chdir(prevdir)
                    return
                rc("display")
                fileCount = 2
            finally:
                os.chdir(prevdir)

        

        #   This callback is called when the user click the 
        #   "Map file" botton. It will display the map file
        #   of input file and change the transparency to 80%.
        def Map_callback():
            global fileCount
            global MSTAE
            global mapOpen
            global MSTcreated_check

            check_MST_created()

            if MSTcreated_check:
                outfilePath = WorkPath.showWorkingPath()
                end = outfilePath.find('/MainMastUI')
                outfilePath = outfilePath[0:int(end)]
                prevdir = os.getcwd()
                newdir = outfilePath + "/MAINMAST/MAINMASTfile"
                situsFile = fileName + ".situs"
                currentSitus = "current.situs"

                try:
                    os.chdir(newdir)
                    fn = currentSitus
                    if not mapOpen:
                        rc("open #15 " + fn)
                        rc("transparency 80,s")
                        mapOpen = 1
                except (IOError),e:
                    tkMessageBox.showwarning("Error", "File Error")

                finally:
                    os.chdir(prevdir)



        #   This callback is called when the user click the 
        #   "Hide Map" botton. It will close the map file.
        def Hide_Map_callback():
            global fileCount
            global MSTAE
            global mapOpen
            outfilePath = WorkPath.showWorkingPath()
            end = outfilePath.find('/MainMastUI')
            outfilePath = outfilePath[0:int(end)]
            prevdir = os.getcwd()
            newdir = outfilePath + "/MAINMAST/MAINMASTfile"

            situsFile = fileName + ".situs"
            currentSitus = "current.situs"

            try:
                os.chdir(newdir)
                fn = currentSitus
                if mapOpen:
                    rc("close #15")
                    mapOpen = 0
            finally:
                os.chdir(prevdir)



        #   This callback is excuted when the user click either
        #   "Create MST & All Edges" or "Create all files" botton.
        #   It takes the values for each parameter from the input
        #   boxes, change the UI display indicating the file is
        #   generating, and then call 'create_file' function to
        #   generate MST and AE files.
        def changeAttri_Callback():
            global filePath
            global outfilePath
            global fileNamePrev
            filePath=efilePath.get()
            fileNamePrev=efileName.get()
            # outfilePath=ofilePath.get()
            outfilePath = WorkPath.showWorkingPath()
            end = outfilePath.find('/MainMastUI')
            # print(end)
            outfilePath = outfilePath[0:int(end)]
            # print(workingPath)
            outfilePath = outfilePath + "/MAINMAST"
            t=et.get()
            Pfilter=ePfilter.get()
            Dkeep=eDkeep.get()
            Ntb=eNtb.get()
            Rlocal=eRlocal.get()
            Nround=eNround.get()
            global MCP_Num
            global CA_Num
            MCP_Num=MCP_Variable.get()
            CA_Num=CA_Variable.get()
            global MSTcreate
            global AEcreate
            global Pathcreate
            global CAcreate
            MSTcreate = Tkinter.Label(createFileUI.sub_frame, text="MST & all Edges:  generating files")
            MSTcreate.grid(row=13, column=0, columnspan=2, sticky=Tkinter.W)
            CAcreate = Tkinter.Label(createFileUI.sub_frame, text="All Files: file not created")
            CAcreate.grid(row=14, column=0, columnspan=2, sticky=Tkinter.W)
            print(filePath,fileNamePrev,outfilePath,t,Pfilter,Dkeep,Ntb,Rlocal,Nround,MCP_Num,CA_Num)
            create_file(filePath,fileNamePrev,t,Pfilter,Dkeep,Ntb,Rlocal,Nround,False)


        #   This callback is excuted when the user click "Create all files" botton.
        #   It takes the values for each parameter from the input boxes, change the
        #   UI display indicating all files are generating, and then call
        #   'create_file' function to generate all files.
        def CA_Create_Callback():

            #   get the variables from the user input boxes. Then change the UI display
            global filePath
            filePath=efilePath.get()
            global fileNamePrev
            fileNamePrev=efileName.get()
            global fileName
            fileName = fileNamePrev.split(".")[0]
            global outfilePath
            outfilePath = WorkPath.showWorkingPath()
            global spd3filePathPrev
            spd3filePathPrev=spd3fileName.get()
            end = outfilePath.find('/MainMastUI')
            outfilePath = outfilePath[0:int(end)]
            outfilePath = outfilePath + "/MAINMAST"
            t=et.get()
            Pfilter=ePfilter.get()
            Dkeep=eDkeep.get()
            Ntb=eNtb.get()
            Rlocal=eRlocal.get()
            Nround=eNround.get()
            global MCP_Num
            global CA_Num
            MCP_Num=MCP_Variable.get()
            CA_Num=CA_Variable.get()
            global MSTcreate
            global AEcreate
            global Pathcreate
            global CAcreate
            MSTcreate = Tkinter.Label(createFileUI.sub_frame, text="MST & all Edges:  generating files")
            MSTcreate.grid(row=13, column=0, columnspan=2, sticky=Tkinter.W)
            CAcreate = Tkinter.Label(createFileUI.sub_frame, text="All Files:  generating files")
            CAcreate.grid(row=14, column=0, columnspan=2, sticky=Tkinter.W)
            print(filePath,fileNamePrev,outfilePath,t,Pfilter,Dkeep,Ntb,Rlocal,Nround,MCP_Num,CA_Num)

            #   Create MST and AE file by calling the 'create_file' function.
            create_file(filePath,fileNamePrev,t,Pfilter,Dkeep,Ntb,Rlocal,Nround,True)

            seqFile = fileName + ".seq"
            spd3File = fileName + ".spd3"
            outfilePath = WorkPath.showWorkingPath()
            end = outfilePath.find('/MainMastUI')
            outfilePath = outfilePath[0:int(end)]
            prevdir = os.getcwd()
            newdir = outfilePath + "/MAINMAST/MAINMASTfile"

            try:
                filename = spd3filePathPrev.split("/")
                spd3path = newdir + "/" + filename[len(filename)-1]
                copyfile(spd3filePathPrev, spd3path)
                spd3File = spd3path
            except:
                print(".seq file Does not exist")


            #   after generate the MST and AE file, we first saperate the 'path.pdb'
            #   into 10 different path models. They will be the 10 different pathes
            #   generated by MAINMAST.
            try:
                os.chdir(newdir)
                i = 0
                fn_sub = "path"+`i`+".pdb"
                file = open(fn_sub,"w")
                with open("path.pdb") as pdbfile:
                    for line in pdbfile:
                        if line[:6] == 'ENDMDL':
                            file.write(line)
                            print("new model")
                            i = i + 1;
                            fn_sub = "path"+`i`+".pdb"
                            try:
                                os.remove(fn_sub)
                            except:
                                print("No such file or directory")
                            if i < 10:
                                file = open(fn_sub,"w")
                        else:
                            file.write(line)


                f = open("CA.pdb", "w")
                caall = subprocess.Popen(["../ThreadCA", "-i", "path.pdb", "-a", "../20AA.param", "-spd", "current.spd3", "-fw", "1.4", "-Ab", "3.4", "-Wb", "0.9"], stdout=f)
                caall.communicate()
                f.close()

                ### Because we are not using the CA reverse file not, So did not create the file to save time ###
                #f = open("CA_r.pdb", "w")
                #subprocess.Popen(["../ThreadCA", "-i", "path.pdb", "-a", "../20AA.param", "-spd", spd3File, "-fw", "1.4", "-Ab", "3.4", "-Wb", "0.9", "-r"], stdout=f)
                #f.close()

                i = 0
                fn_sub = "CA"+`i`+".pdb"
                #fnr_sub = "CA_r"+`i`+".pdb"
                file = open(fn_sub,"w")
                while (i < 10):
                    pathFile = "path"+`i`+".pdb"
                    f = open(fn_sub, "w")
                    ca = subprocess.Popen(["../ThreadCA", "-i", pathFile, "-a", "../20AA.param", "-spd", "current.spd3", "-fw", "1.4", "-Ab", "3.4", "-Wb", "0.9"], stdout=f)
                    ca.communicate()
                    f.close()
                    #f = open(fnr_sub, "w")
                    #subprocess.Popen(["../ThreadCA", "-i", pathFile, "-a", "../20AA.param", "-spd", spd3File, "-fw", "1.4", "-Ab", "3.4", "-Wb", "0.9", "-r"], stdout=f)
                    #f.close()
                    i = i + 1
                    fn_sub = "CA"+`i`+".pdb"
                    #fnr_sub = "CA_r"+`i`+".pdb"

                if "darwin" in platform.lower():
                    subprocess.Popen(["../pulchra/bin/osx/pulchra", "CA.pdb"])
                elif "linux" in platform.lower():
                    subprocess.Popen(["../pulchra/bin/linux/pulchra", "CA.pdb"])
                else:
                    tkMessageBox.showwarning("Warning","Unknow platform: no supporting pulchra file")

            finally:
                CAcreate = Tkinter.Label(createFileUI.sub_frame, text="All Files: ready to display")
                CAcreate.grid(row=14, column=0, columnspan=2, sticky=Tkinter.W)
                os.chdir(prevdir)


        #   This callback is called when the user select the input file.
        #   It pops up a file selection window and allow the user to
        #   navigate to the find the file.
        def chooseFile_callback():
            path=tkFileDialog.askopenfilename()
            if path != "":
                efileName.delete(0, "end")
                efilePath.delete(0, "end")
                
                filename = path.split("/")
                efileName.insert(0, filename[len(filename)-1])
                efilePath.insert(0, path)
                pnix_mrc.delete(0, "end")


        def chooseMrcFile_callback():
            path=tkFileDialog.askopenfilename()
            if path != "":
                pnix_mrc.delete(0, "end")
                
                if path == "":
                    return
                pnix_mrc.insert(0, path)

                outfilePath = WorkPath.showWorkingPath()
                end = outfilePath.find('/MainMastUI')
                outfilePath = outfilePath[0:int(end)]
                prevdir = os.getcwd()
                newdir = outfilePath + "/MAINMAST/MAINMASTfile"

                copyfile(path, newdir + "/current.mrc")


        #   This callback is called when the user select the input spd3 file.
        #   It pops up a file selection window and allow the user to
        #   navigate to the find the file.
        def chooseSpd3File_callback():
            spd3fileName.delete(0, "end")
            spd3filePath.delete(0, "end")
            path=tkFileDialog.askopenfilename()
            filename = path.split("/")
            spd3fileName.insert(0, path)

        def compare_file1_callback():
            global select_file1_Name

            path=tkFileDialog.askdirectory()
            if path != "":
                select_file1_Name.delete(0, "end")
                select_file1_Name.insert(0, path)

        def compare_file2_callback():
            global select_file2_Name

            path=tkFileDialog.askdirectory()
            if path != "":
                select_file2_Name.delete(0, "end")
                select_file2_Name.insert(0, path)

        def compare_file3_callback():
            global select_file3_Name

            path=tkFileDialog.askdirectory()
            if path != "":
                select_file3_Name.delete(0, "end")
                select_file3_Name.insert(0, path)

        #   this callback is called when the user click "Minimum Spanning Tree" in
        #   "compare history files" window. It will show up to 3 MST graph selected
        #   by user.
        def compare_MST_callback():
            global select1
            global select2
            global select3
            global select_file1_Name
            global select_file2_Name
            global select_file3_Name
            global MSTAE

            MSTAE = 0
            workingPath = WorkPath.showWorkingPath()
            end = workingPath.find('/MainMastUI')
            workingPath = workingPath[0:int(end)]
            workingPath = workingPath + "/MAINMAST/history/"

            compare1 = select1.get().rstrip()
            compare2 = select2.get().rstrip()
            compare3 = select3.get().rstrip()

            comp_path_1 = select_file1_Name.get()

            comp_path_2 = select_file2_Name.get()

            comp_path_3 = select_file3_Name.get()

            print(comp_path_1)
            print(comp_path_2)
            print(comp_path_3)


            rc("close all");

            if comp_path_1 != "":
                prevdir = os.getcwd()
                try:
                    os.chdir(comp_path_1)
                    fn = "tree.pdb"
                    modelcompMST1=chimera.openModels.open(fn)
                    try:
                        res=modelcompMST1[0].residues
                    except:
                        print("file not ready yet")
                    rc("~bond")
                    rc("display #0")
                    with open("tree.pdb") as pdbfile:
                        grp=getPseudoBondGroup("compMST1", associateWith=modelcompMST1)
                        for line in pdbfile:
                            if line[:4] == 'BOND':
                                grp.newPseudoBond(res[int(line[7:11])-1].atomsMap['CA'][0], res[int(line[13:17])-1].atomsMap['CA'][0])
                    rc("repr bs")
                    rc("vdwdefine 1")
                finally:
                    os.chdir(prevdir)


            if comp_path_2 != "":
                prevdir = os.getcwd()
                try:
                    os.chdir(comp_path_2)
                    fn = "tree.pdb"
                    modelcompMST2=chimera.openModels.open(fn)
                    try:
                        res=modelcompMST2[0].residues
                    except:
                        print("file not ready yet")
                    rc("~bond")
                    rc("display #1")
                    with open("tree.pdb") as pdbfile:
                        grp=getPseudoBondGroup("compMST2", associateWith=modelcompMST2)
                        for line in pdbfile:
                            if line[:4] == 'BOND':
                                grp.newPseudoBond(res[int(line[7:11])-1].atomsMap['CA'][0], res[int(line[13:17])-1].atomsMap['CA'][0])
                    rc("repr bs")
                    rc("vdwdefine 1")
                finally:
                    os.chdir(prevdir)


            if comp_path_3 != "":
                prevdir = os.getcwd()
                try:
                    os.chdir(comp_path_3)
                    fn = "tree.pdb"
                    modelcompMST3=chimera.openModels.open(fn)
                    try:
                        res=modelcompMST3[0].residues
                    except:
                        print("file not ready yet")
                    rc("~bond")
                    rc("display #0")
                    with open("tree.pdb") as pdbfile:
                        grp=getPseudoBondGroup("compMST3", associateWith=modelcompMST3)
                        for line in pdbfile:
                            if line[:4] == 'BOND':
                                grp.newPseudoBond(res[int(line[7:11])-1].atomsMap['CA'][0], res[int(line[13:17])-1].atomsMap['CA'][0])
                    rc("repr bs")
                    rc("vdwdefine 1")
                finally:
                    os.chdir(prevdir)


        #   this callback is called when the user click "All edges" in
        #   "compare history files" window. It will show up to 3 AE graph selected
        #   by user.
        def compare_AE_callback():
            global select1
            global select2
            global select3
            global select_file1_Name
            global select_file2_Name
            global select_file3_Name
            global MSTAE

            MSTAE = 0
            workingPath = WorkPath.showWorkingPath()
            end = workingPath.find('/MainMastUI')
            workingPath = workingPath[0:int(end)]
            workingPath = workingPath + "/MAINMAST/history/"

            compare1 = select1.get().rstrip()
            compare2 = select2.get().rstrip()
            compare3 = select3.get().rstrip()

            comp_path_1 = select_file1_Name.get()

            comp_path_2 = select_file2_Name.get()

            comp_path_3 = select_file3_Name.get()


            rc("close all");

            if comp_path_1 != "":
                print("compare 1")
                prevdir = os.getcwd()
                try:
                    os.chdir(comp_path_1)
                    fn = "graph.pdb"
                    modelcompAE1=chimera.openModels.open(fn)
                    try:
                        res=modelcompAE1[0].residues
                    except:
                        print("file not ready yet")
                    rc("~bond")
                    rc("display #0")
                    with open("graph.pdb") as pdbfile:
                        grp=getPseudoBondGroup("compAE1", associateWith=modelcompAE1)
                        for line in pdbfile:
                            if line[:4] == 'BOND':
                                grp.newPseudoBond(res[int(line[7:11])-1].atomsMap['CA'][0], res[int(line[13:17])-1].atomsMap['CA'][0])
                    rc("repr bs")
                    rc("vdwdefine 1")
                finally:
                    os.chdir(prevdir)


            if comp_path_2 != "":
                print("compare 2")
                prevdir = os.getcwd()
                try:
                    os.chdir(comp_path_2)
                    fn = "graph.pdb"
                    modelcompAE2=chimera.openModels.open(fn)
                    try:
                        res=modelcompAE2[0].residues
                    except:
                        print("file not ready yet")
                    rc("~bond")
                    rc("display #1")
                    with open("graph.pdb") as pdbfile:
                        grp=getPseudoBondGroup("compAE2", associateWith=modelcompAE2)
                        for line in pdbfile:
                            if line[:4] == 'BOND':
                                grp.newPseudoBond(res[int(line[7:11])-1].atomsMap['CA'][0], res[int(line[13:17])-1].atomsMap['CA'][0])
                    rc("repr bs")
                    rc("vdwdefine 1")
                finally:
                    os.chdir(prevdir)


            if comp_path_3 != "":
                prevdir = os.getcwd()
                try:
                    os.chdir(comp_path_3)
                    fn = "graph.pdb"
                    modelcompAE3=chimera.openModels.open(fn)
                    try:
                        res=modelcompAE3[0].residues
                    except:
                        print("file not ready yet")
                    rc("~bond")
                    rc("display #0")
                    with open("graph.pdb") as pdbfile:
                        grp=getPseudoBondGroup("compAE3", associateWith=modelcompAE3)
                        for line in pdbfile:
                            if line[:4] == 'BOND':
                                grp.newPseudoBond(res[int(line[7:11])-1].atomsMap['CA'][0], res[int(line[13:17])-1].atomsMap['CA'][0])
                    rc("repr bs")
                    rc("vdwdefine 1")
                finally:
                    os.chdir(prevdir)


        #   this callback is called when the user click "Main-Chain Paths" in
        #   "compare history files" window. It will show up to 3 Main Chain Path
        #   graph selected by user.
        def compare_MCP_callback():
            global select1
            global select2
            global select3
            global select_file1_Name
            global select_file2_Name
            global select_file3_Name
            global MSTAE

            MSTAE = 0
            workingPath = WorkPath.showWorkingPath()
            end = workingPath.find('/MainMastUI')
            workingPath = workingPath[0:int(end)]
            workingPath = workingPath + "/MAINMAST/history/"

            compare1 = select1.get().rstrip()
            compare2 = select2.get().rstrip()
            compare3 = select3.get().rstrip()

            comp_path_1 = select_file1_Name.get()

            comp_path_2 = select_file2_Name.get()

            comp_path_3 = select_file3_Name.get()

            rc("close all");

            if comp_path_1 != "":
                print("compare 1")
                prevdir = os.getcwd()
                try:
                    os.chdir(comp_path_1)
                    fn = "path0.pdb"
                    modelMCP1=chimera.openModels.open(fn)
                except (IOError ,ZeroDivisionError),e:
                    print("no path.pdb")
                finally:
                    os.chdir(prevdir)


            if comp_path_2 != "":
                print("compare 2")
                prevdir = os.getcwd()
                try:
                    os.chdir(comp_path_2)
                    fn = "path0.pdb"
                    modelMCP2=chimera.openModels.open(fn)
                except (IOError ,ZeroDivisionError),e:
                    print("no path.pdb")
                finally:
                    os.chdir(prevdir)


            if comp_path_3 != "":
                prevdir = os.getcwd()
                try:
                    os.chdir(comp_path_3)
                    fn = "path0.pdb"
                    modelMCP3=chimera.openModels.open(fn)
                except (IOError ,ZeroDivisionError),e:
                    print("no path.pdb")
                finally:
                    os.chdir(prevdir)


        #   this callback is called when the user click "CA models" in
        #   "compare history files" window. It will show up to 3 CA model
        #   graph selected by user.
        def compare_CA_callback():
            global select1
            global select2
            global select3
            global select_file1_Name
            global select_file2_Name
            global select_file3_Name
            global MSTAE

            MSTAE = 0
            workingPath = WorkPath.showWorkingPath()
            end = workingPath.find('/MainMastUI')
            workingPath = workingPath[0:int(end)]
            workingPath = workingPath + "/MAINMAST/history/"

            compare1 = select1.get().rstrip()
            compare2 = select2.get().rstrip()
            compare3 = select3.get().rstrip()

            comp_path_1 = select_file1_Name.get()

            comp_path_2 = select_file2_Name.get()

            comp_path_3 = select_file3_Name.get()

            rc("close all");

            if comp_path_1 != "":
                print("compare 1")
                prevdir = os.getcwd()
                try:
                    os.chdir(comp_path_1)
                    fn = "CA.pdb"
                    modelCA1=chimera.openModels.open(fn)
                except (IOError ,ZeroDivisionError),e:
                    print("no CA.pdb")
                finally:
                    os.chdir(prevdir)


            if comp_path_2 != "":
                print("compare 2")
                prevdir = os.getcwd()
                try:
                    os.chdir(comp_path_2)
                    fn = "CA.pdb"
                    modelCA2=chimera.openModels.open(fn)
                except (IOError ,ZeroDivisionError),e:
                    print("no CA.pdb")
                finally:
                    os.chdir(prevdir)


            if comp_path_3 != "":
                prevdir = os.getcwd()
                try:
                    os.chdir(comp_path_3)
                    fn = "CA.pdb"
                    modelCA3=chimera.openModels.open(fn)
                except (IOError ,ZeroDivisionError),e:
                    print("no CA.pdb")
                finally:
                    os.chdir(prevdir)

        

        #   this callback is called when the user click "All Atom Models" in
        #   "compare history files" window. It will show up to 3 CA_rebuilt
        #   graphs selected by user. This only works when the user has pulchra
        #   refinement build in.
        def compare_CArebuilt_callback():
            global select1
            global select2
            global select3
            global select_file1_Name
            global select_file2_Name
            global select_file3_Name
            global MSTAE

            MSTAE = 0
            workingPath = WorkPath.showWorkingPath()
            end = workingPath.find('/MainMastUI')
            workingPath = workingPath[0:int(end)]
            workingPath = workingPath + "/MAINMAST/history/"

            compare1 = select1.get().rstrip()
            compare2 = select2.get().rstrip()
            compare3 = select3.get().rstrip()

            comp_path_1 = select_file1_Name.get()

            comp_path_2 = select_file2_Name.get()

            comp_path_3 = select_file3_Name.get()

            rc("close all");

            if comp_path_1 != "":
                print("compare 1")
                prevdir = os.getcwd()
                try:
                    os.chdir(comp_path_1)
                    fn = "CA.rebuilt.pdb"
                    if os.path.exists(fn):
                        modelCArebuilt1=chimera.openModels.open(fn)
                except (IOError ,ZeroDivisionError),e:
                    print("no CA.rebuilt.pdb")
                finally:
                    os.chdir(prevdir)


            if comp_path_2 != "":
                print("compare 2")
                prevdir = os.getcwd()
                try:
                    os.chdir(comp_path_2)
                    fn = "CA.rebuilt.pdb"
                    if os.path.exists(fn):
                        modelCArebuilt2=chimera.openModels.open(fn)
                except (IOError ,ZeroDivisionError),e:
                    print("no CA.rebuilt.pdb")
                finally:
                    os.chdir(prevdir)

            if comp_path_3 != "":
                prevdir = os.getcwd()
                try:
                    os.chdir(comp_path_3)
                    fn = "CA.rebuilt.pdb"
                    if os.path.exists(fn):
                        modelCArebuilt3=chimera.openModels.open(fn)
                except (IOError ,ZeroDivisionError),e:
                    print("no CA.rebuilt.pdb")
                finally:
                    os.chdir(prevdir)

            rc("display")


        #   This callback is called when the user click "save session&file" botton.
        #   It will save the file to the directory of user's choice.
        def Save_callback():
            fileNamePrev=efileName.get()
            t=et.get()
            Pfilter=ePfilter.get()
            Dkeep=eDkeep.get()
            Ntb=eNtb.get()
            Rlocal=eRlocal.get()
            Nround=eNround.get()
            spd3filePathPrev=spd3fileName.get()
            Pnix = pnix.get()
            PnixMrc = pnix_mrc.get()
            fileName = fileNamePrev.split(".situs")

            global MSTcreated_check
            global currentFileStored

            check_MST_created()

            if not MSTcreated_check:
                return

            path=tkFileDialog.asksaveasfilename(title='save file to directory',initialfile = fileName[0] + "_with_" + t + "t")
            print(path)
            if path != "":

                path = path + "/MAINMASTfile_" + fileName[0] + "@" + t + "t"
                

                outfilePath = WorkPath.showWorkingPath()
                end = outfilePath.find('/MainMastUI')
                outfilePath = outfilePath[0:int(end)]
                prevdir = os.getcwd()
                newdir = outfilePath + "/MAINMAST/MAINMASTfile"

                try:
                    copy_tree(newdir, path)

                    command = "save " + path + "/" + fileName[0] + "_with_" + t + "t" + "_session.py"
                    rc(command)
                    var_file = path + "/var_file.txt"

                    create_info_1 = CAcreate.cget("text");
                    if "ready to display" in create_info_1:
                        var_specs = "CA~~~" + fileNamePrev + "~~~" + t + "~~~" + Pfilter + "~~~" + Dkeep + "~~~" + Ntb + "~~~" + Rlocal + "~~~" + Nround + "~~~" + spd3filePathPrev + "~~~" + Pnix + "~~~" + PnixMrc 
                    else:
                        var_specs = "MST~~~" + fileNamePrev + "~~~" + t + "~~~" + Pfilter + "~~~" + Dkeep + "~~~" + Ntb + "~~~" + Rlocal + "~~~" + Nround + "~~~" + spd3filePathPrev + "~~~" + Pnix + "~~~" + PnixMrc 


                    with open(var_file,'a') as variable_file:
                        variable_file.write(var_specs)
                    currentFileStored = 1

                    tkMessageBox.showinfo("Success", "session saved to " + path)
                except:
                    tkMessageBox.showwarning("Error", "Save file error")
                    return


        def Restore_and_change_attribute(path):
            global MSTcreate
            global CAcreate
            global restored_from_file

            pathSplit = path.split("/")
            print(path)
            print(pathSplit[len(pathSplit) - 1])
            _index = pathSplit[len(pathSplit) - 1].find("_")
            pyfile = [ f for f in os.listdir(path) if f.endswith("session.py") ]
            print(pyfile)
            filedir = path
            try:
                command = "open " + path + "/" + pyfile[0]
            except:
                tkMessageBox.showwarning("Error", "File not found. Please make sure to choose the parent folder where you store the file.")
                return
            try:
                outfilePath = WorkPath.showWorkingPath()
                end = outfilePath.find('/MainMastUI')
                outfilePath = outfilePath[0:int(end)]
                newdir = outfilePath + "/MAINMAST/MAINMASTfile"
                filelist = [ file for file in os.listdir(newdir) ]
                for f in filelist:
                    os.remove(os.path.join(newdir, f))
                copy_tree(path, newdir)
                print(command)
                rc(command)
                MSTAE = 0
                pyfile = [ f for f in os.listdir(newdir) if f.endswith("session.py") or f.endswith("session.pyc") ]
                for f in pyfile:
                    os.remove(os.path.join(newdir, f))

            

                varlist = ""
                var_file = path + "/var_file.txt"
                with open(var_file,'r') as variable_file:
                    varlist = variable_file.readline()
                var_list = varlist.split("~~~")
                if var_list[0] == "CA":
                    MSTcreate = Tkinter.Label(createFileUI.sub_frame, text="MST & all Edges: ready to display")
                    MSTcreate.grid(row=13, column=0, columnspan=2, sticky=Tkinter.W)

                    CAcreate = Tkinter.Label(createFileUI.sub_frame, text="All Files: ready to display")
                    CAcreate.grid(row=14, column=0, columnspan=2, sticky=Tkinter.W)
                else:
                    MSTcreate = Tkinter.Label(createFileUI.sub_frame, text="MST & all Edges: ready to display")
                    MSTcreate.grid(row=13, column=0, columnspan=2, sticky=Tkinter.W)

                    CAcreate = Tkinter.Label(createFileUI.sub_frame, text="All Files: file not created")
                    CAcreate.grid(row=14, column=0, columnspan=2, sticky=Tkinter.W)
                efileName.delete(0, "end")
                efilePath.delete(0, "end")
                et.delete(0, "end")
                ePfilter.delete(0, "end")
                eDkeep.delete(0, "end")
                eNtb.delete(0, "end")
                eRlocal.delete(0, "end")
                eNround.delete(0, "end")
                spd3fileName.delete(0, "end")
                pnix.delete(0, "end")
                pnix_mrc.delete(0, "end")

                efileName.insert(0, var_list[1])
                efilePath.insert(0, filedir + "/" + var_list[1])
                et.insert(0, var_list[2])
                ePfilter.insert(0, var_list[3])
                eDkeep.insert(0, var_list[4])
                eNtb.insert(0, var_list[5])
                eRlocal.insert(0, var_list[6])
                eNround.insert(0, var_list[7])
                splitvar = var_list[8].split("/")
                var_list[8] = splitvar[len(splitvar) - 1]
                spd3fileName.insert(0, filedir + "/" + var_list[8])
                pnix.insert(0, var_list[9])
                if var_list[10] != "":
                    splitvar = var_list[10].split("/")
                    var_list[10] = splitvar[len(splitvar) - 1]
                    pnix_mrc.insert(0, filedir + "/" + var_list[10])
                else:
                    pnix_mrc.insert(0, "")
                restored_from_file = 1
                MSTAE = 1

                

                os.remove(newdir + "/var_file.txt")
            except:
                tkMessageBox.showwarning("Error", "Restore file error")
                return

        #   This callback is called when the user click "restore session&file" botton.
        #   It will pop up a directory selection window asking users to select file.
        #   If the file is in the correct form, the program will restore the graphs
        #   with stored orientation.
        def Restore_callback():
            global MSTAE
            path=tkFileDialog.askdirectory()
            if path != "":
                Restore_and_change_attribute(path)
            


        #   This popup will be triggered if the value of parameter inputs are not
        #   number or the number is out of range. If the inputs are numbers and are
        #   in range, it will call 'changeAttri_Callback()' to generate MST and AE.
        def check_value_popup():
            global check_value_popup

            # store_file_before_next_create()

            fileNamePrev=efileName.get()
            pnixWeight=pnix.get()
            t=et.get()
            Pfilter=ePfilter.get()
            Dkeep=eDkeep.get()
            Ntb=eNtb.get()
            Rlocal=eRlocal.get()
            Nround=eNround.get()
            var_check = 1;
            
            if fileNamePrev=="":
                tkMessageBox.showwarning("Warning", "MAP file and spd3 file cannot be empty");
                var_check = 0;

            if not (is_number(t) and (is_number(Pfilter)) and (is_number(Dkeep)) and (is_number(Ntb)) and (is_number(Rlocal)) and is_number(Nround)):
                tkMessageBox.showwarning("Warning", "parameter values must be number")
                var_check = 0;

            else:
                if not ((0 < float(t) < 1000) and (0 < float(Pfilter) < 1000) and (0 < float(Dkeep) < 1000) and (0 < float(Ntb) < 1000) and (0 < float(Rlocal) < 1000) and (0 < float(Nround) < 1000)):
                    tkMessageBox.showwarning("Warning", "parameter values should be in range (0, 1000)");
                    var_check = 0;

            if var_check:
                changeAttri_Callback()


        #   This popup will be triggered if the value of parameter inputs are not
        #   number or the number is out of range. If the inputs are numbers and are
        #   in range, it will call 'CA_Create_Callback()' to generate all files.
        def check_value_popup_CA():
            global check_value_popup

            # store_file_before_next_create()


            fileNamePrev=efileName.get()
            pnixWeight=pnix.get()
            t=et.get()
            Pfilter=ePfilter.get()
            Dkeep=eDkeep.get()
            Ntb=eNtb.get()
            Rlocal=eRlocal.get()
            Nround=eNround.get()
            var_check = 1;
            
            if fileNamePrev=="":
                tkMessageBox.showwarning("Warning", "MAP file and spd3 file cannot be empty");
                var_check = 0;

            if not (is_number(t) and (is_number(Pfilter)) and (is_number(Dkeep)) and (is_number(Ntb)) and (is_number(Rlocal)) and is_number(Nround)):
                tkMessageBox.showwarning("Warning", "parameter values must be number")
                var_check = 0;

            else:
                if not ((0 < float(t) < 1000) and (0 < float(Pfilter) < 1000) and (0 < float(Dkeep) < 1000) and (0 < float(Ntb) < 1000) and (0 < float(Rlocal) < 1000) and (0 < float(Nround) < 1000)):
                    tkMessageBox.showwarning("Warning", "parameter values should be in range (0, 1000)");
                    var_check = 0;


            if var_check:
                CA_Create_Callback();

        def save_and_check_value():
            Save_callback()
            close_storeFilePopUp()
            # check_value_popup()

        def save_and_check_value_CA():
            Save_callback()
            close_storeFilePopUp_CA()
            # check_value_popup_CA()

        def save_and_check_value_Restore():
            Save_callback()
            close_storeFilePopUp_Restore()

        def save_and_check_value_Compare():
            Save_callback()
            close_storeFilePopUp_Compare()


        def store_file_before_restore():
            global storeFilePopUp
            global currentFileStored
            global restored_from_file

            create_info_1 = MSTcreate.cget("text");

            if not currentFileStored and not restored_from_file:
                if "ready to display" in create_info_1:
                    storeFilePopUp = Toplevel()
                    label1 = Label(storeFilePopUp, text="Save current files before restore files?", height=2)
                    SaveH_Button = Tkinter.Button(storeFilePopUp, text="save", width=16, height=2, command=save_and_check_value_Restore)
                    noSaveH_Button = Tkinter.Button(storeFilePopUp, text="do not save", width=16, height=2, command=close_storeFilePopUp_Restore)
                    label1.grid(row=1,column=0, columnspan=2, sticky=Tkinter.W)
                    SaveH_Button.grid(row=3,column=0)
                    noSaveH_Button.grid(row=3,column=1)
                else:
                    Restore_callback()
            else:
                Restore_callback()


        def store_file_before_compare():
            global storeFilePopUp
            global currentFileStored
            global restored_from_file

            create_info_1 = MSTcreate.cget("text");

            if not currentFileStored and not restored_from_file:
                if "ready to display" in create_info_1:
                    storeFilePopUp = Toplevel()
                    label1 = Label(storeFilePopUp, text="Save current files before compare files?", height=2)
                    SaveH_Button = Tkinter.Button(storeFilePopUp, text="save", width=16, height=2, command=save_and_check_value_Compare)
                    noSaveH_Button = Tkinter.Button(storeFilePopUp, text="do not save", width=16, height=2, command=close_storeFilePopUp_Compare)
                    label1.grid(row=1,column=0, columnspan=2, sticky=Tkinter.W)
                    SaveH_Button.grid(row=3,column=0)
                    noSaveH_Button.grid(row=3,column=1)
                else:
                    Compare_file_callback()
            else:
                Compare_file_callback()


        def store_file_before_next_create():
            global storeFilePopUp
            global currentFileStored
            global restored_from_file

            create_info_1 = MSTcreate.cget("text");

            if not currentFileStored and not restored_from_file:
                if "ready to display" in create_info_1:
                    storeFilePopUp = Toplevel()
                    label1 = Label(storeFilePopUp, text="Save current files before creating new files?", height=2)
                    SaveH_Button = Tkinter.Button(storeFilePopUp, text="save", width=16, height=2, command=save_and_check_value)
                    noSaveH_Button = Tkinter.Button(storeFilePopUp, text="do not save", width=16, height=2, command=close_storeFilePopUp)
                    label1.grid(row=1,column=0, columnspan=2, sticky=Tkinter.W)
                    SaveH_Button.grid(row=3,column=0)
                    noSaveH_Button.grid(row=3,column=1)
                else:
                    check_value_popup()
            else:
                check_value_popup()


        def store_file_before_next_create_CA():
            global storeFilePopUp
            global currentFileStored
            global restored_from_file

            create_info_1 = MSTcreate.cget("text");

            if not currentFileStored and not restored_from_file:
                print("here")
                if "ready to display" in create_info_1:
                    storeFilePopUp = Toplevel()
                    label1 = Label(storeFilePopUp, text="Save current files before creating new files?", height=2)
                    SaveH_Button = Tkinter.Button(storeFilePopUp, text="save", width=16, height=2, command=save_and_check_value_CA)
                    noSaveH_Button = Tkinter.Button(storeFilePopUp, text="do not save", width=16, height=2, command=close_storeFilePopUp_CA)
                    label1.grid(row=1,column=0, columnspan=2, sticky=Tkinter.W)
                    SaveH_Button.grid(row=3,column=0)
                    noSaveH_Button.grid(row=3,column=1)
                else:
                    check_value_popup_CA()
            else:
                check_value_popup_CA()

        def close_storeFilePopUp():
            global storeFilePopUp
            storeFilePopUp.destroy()
            check_value_popup()

        def close_storeFilePopUp_CA():
            global storeFilePopUp
            storeFilePopUp.destroy()
            check_value_popup_CA()

        def close_storeFilePopUp_Restore():
            global storeFilePopUp
            storeFilePopUp.destroy()
            Restore_callback()

        def close_storeFilePopUp_Compare():
            global storeFilePopUp
            storeFilePopUp.destroy()
            Compare_file_callback()



        #   This callback is called when the user click "save files to history" botton.
        #   It will popup a window showing the current parameters user used to generate
        #   the graph and asking if the user want to save the file to history.
        def Save_History_callback():
            global saveHistoryPopUp
            global history_name
            fileNamePrev=efileName.get()
            t=et.get()
            Pfilter=ePfilter.get()
            Dkeep=eDkeep.get()
            Ntb=eNtb.get()
            Rlocal=eRlocal.get()
            Nround=eNround.get()
            workingPath = WorkPath.showWorkingPath()
            end = workingPath.find('/MainMastUI')
            workingPath = workingPath[0:int(end)]
            workingPath = workingPath + "/MAINMAST"
            his_path = workingPath + "/history/"

            saveHistoryPopUp = Toplevel()
            label1 = Label(saveHistoryPopUp, text="Save the output files to history:", height=2)
            label1.grid(row=1,column=1, columnspan=2, sticky=Tkinter.W)

            Tkinter.Label(saveHistoryPopUp, text="Input file name:  " + fileNamePrev).grid(row=2,column=1, columnspan=2, sticky=Tkinter.W)

            Tkinter.Label(saveHistoryPopUp, text="Threshold of density values:  " + t).grid(row=3,column=1, columnspan=2, sticky=Tkinter.W)

            Tkinter.Label(saveHistoryPopUp, text="Filter of representative points:  " + Pfilter).grid(row=4,column=1, columnspan=2, sticky=Tkinter.W)

            Tkinter.Label(saveHistoryPopUp, text="Maximum Edge distance:  " + Dkeep).grid(row=5,column=1, columnspan=2, sticky=Tkinter.W)

            Tkinter.Label(saveHistoryPopUp, text="Size of tabu-list:  " + Ntb).grid(row=6,column=1, columnspan=2, sticky=Tkinter.W)

            Tkinter.Label(saveHistoryPopUp, text="Radius of Local MST:  " + Rlocal).grid(row=7,column=1, columnspan=2, sticky=Tkinter.W)

            Tkinter.Label(saveHistoryPopUp, text="Number of Iterations:  " + Nround).grid(row=8,column=1, columnspan=2, sticky=Tkinter.W)

            SaveH_Button = Tkinter.Button(saveHistoryPopUp, text="save", width=33, height=2, command=Save_to_his_callback)
            SaveH_Button.grid(row=8,column=2, columnspan=2)

            history_name = fileNamePrev + ",t_" + t + ",filter_" + Pfilter + ",Dkeep_" + Dkeep + ",Ntb_" + Ntb + ",Rlocal_" + Rlocal + ",Nround_" + Nround



        #   This callback is called when the user click "save" botton in "save to file" popup.
        #   It will all graphs in the 'history' folder in 'MainMastfile'
        def Save_to_his_callback():
            global saveHistoryPopUp
            global history_name
            workingPath = WorkPath.showWorkingPath()
            end = workingPath.find('/MainMastUI')
            workingPath = workingPath[0:int(end)]
            workingPath = workingPath + "/MAINMAST"
            his_file = workingPath + "/history_file.txt"
            his_path = workingPath + "/history/" + history_name
            file_path = workingPath + "/MAINMASTfile"
            history_name = history_name + '\n'


            with open(his_file,'a') as history_file:
                history_file.write(history_name)

            copy_tree(file_path, his_path)
            tkMessageBox.showinfo("Success", "file saved to " + his_path + history_name)

            saveHistoryPopUp.destroy()


        #   This callback is called when the user click "compare history files" botton.
        #   It will popup a window for user to perform compare history task. The window
        #   allows user to choose up to 3 history files to compare with each other.
        #   The graphs available for compare will include "Minimum Spanning Trees",
        #   "All edges", "Main-Chain Paths", "CA models" and "All Atom Models".
        def Compare_file_callback():
            global compareHistoryPopUp
            global history_name
            global select1
            global select2
            global select3
            global select_file1_Name
            global select_file2_Name
            global select_file3_Name
            fileNamePrev=efileName.get()
            t=et.get()
            Pfilter=ePfilter.get()
            Dkeep=eDkeep.get()
            Ntb=eNtb.get()
            Rlocal=eRlocal.get()
            Nround=eNround.get()

            compareHistoryPopUp = Toplevel()

            label1 = Label(compareHistoryPopUp, text="Select files to compare:", height=2)
            label1.grid(row=1,column=0, columnspan=5, sticky=Tkinter.W)

            workingPath = WorkPath.showWorkingPath()
            end = workingPath.find('/MainMastUI')
            workingPath = workingPath[0:int(end)]
            workingPath = workingPath + "/MAINMAST"

            select_file1_Name = Tkinter.Entry(compareHistoryPopUp)
            select_file1_Name.config(width=40)
            select_file1_Name.grid(row=2, column=0, columnspan=4)
            select_file1_Button = Tkinter.Button(compareHistoryPopUp, text="select", width=8, height=1, command=compare_file1_callback)
            select_file1_Button.grid(row=2, column=4)

            select_file2_Name = Tkinter.Entry(compareHistoryPopUp)
            select_file2_Name.config(width=40)
            select_file2_Name.grid(row=3, column=0, columnspan=4)
            select_file2_Button = Tkinter.Button(compareHistoryPopUp, text="select", width=8, height=1, command=compare_file2_callback)
            select_file2_Button.grid(row=3, column=4)

            select_file3_Name = Tkinter.Entry(compareHistoryPopUp)
            select_file3_Name.config(width=40)
            select_file3_Name.grid(row=4, column=0, columnspan=4)
            select_file3_Button = Tkinter.Button(compareHistoryPopUp, text="select", width=8, height=1, command=compare_file3_callback)
            select_file3_Button.grid(row=4, column=4)


            select1 = Tkinter.StringVar(compareHistoryPopUp)
            select1.set("select")
            select2 = Tkinter.StringVar(compareHistoryPopUp)
            select2.set("select")
            select3 = Tkinter.StringVar(compareHistoryPopUp)
            select3.set("select")

            label1 = Label(compareHistoryPopUp, text="Select one to compare:", height=2)
            label1.grid(row=5,column=0, columnspan=5, sticky=Tkinter.W)

            MST_Compare = Tkinter.Button(compareHistoryPopUp, text="Minimum Spanning Trees", wraplength=80, width=8, height=3, command=compare_MST_callback)

            MST_Compare.grid(row=6, column=0, rowspan=2)

            AE_Compare = Tkinter.Button(compareHistoryPopUp, text="All edges", wraplength=80, width=8, height=3, command=compare_AE_callback)

            AE_Compare.grid(row=6, column=1)

            MCP_Compare = Tkinter.Button(compareHistoryPopUp, text="Main-Chain Paths", wraplength=80, width=8, height=3, command=compare_MCP_callback)

            MCP_Compare.grid(row=6, column=2)

            CA_Compare = Tkinter.Button(compareHistoryPopUp, text="CA models", wraplength=80, width=8, height=3, command=compare_CA_callback)

            CA_Compare.grid(row=6, column=3)

            pultura_Compare = Tkinter.Button(compareHistoryPopUp, text="All Atom Models", wraplength=80, width=8, height=3, command=compare_CArebuilt_callback)

            pultura_Compare.grid(row=6, column=4)

            #   Phenix compare botton was deleted because unable to lead module for phenix refinement
            # refine_Compare = Tkinter.Button(compareHistoryPopUp, text="Phenix refinement models", wraplength=80, width=8, height=3, command=MST_callback)

            # refine_Compare.grid(row=6, column=5)



        #   this callback is called when the user click "start Phenix refinement" botton.
        #   Because the error with phython load module, the callback has been changed to
        #   provide the code to the user so they can just copy+paste the code to the terminal
        #   to run Phenix refinement.
        def pnixW_callback():
            outfilePath = WorkPath.showWorkingPath()
            end = outfilePath.find('/MainMastUI')
            outfilePath = outfilePath[0:int(end)]
            outfilePath = outfilePath + "/MAINMAST/MAINMASTfile"
            pnixWeight=pnix.get()
            PnixMrc = pnix_mrc.get()

            if PnixMrc == "":
                tkMessageBox.showwarning("Warning","Please select a .mrc file\n")
                return


            global CAcreated_check

            check_CA_created()

            if not CAcreated_check:
                return

            toplevel = Toplevel()
            label1 = Label(toplevel, text="Instruction about doing Phenix Refinement:", height=2)
            label1.grid(row=1,column=1, columnspan=2, sticky=Tkinter.W)

            label2 = Label(toplevel, text="Command: ", height=2)
            label2.grid(row=2,column=1, columnspan=2, sticky=Tkinter.W)

            label5 = Tkinter.Entry(toplevel, width=100)
            label5.insert(0, "cd " + outfilePath)
            label5.grid(row=3,column=1, columnspan=2, sticky=Tkinter.W)

            label3 = Tkinter.Entry(toplevel, width=100)
            label3.insert(0, "module load phenix")
            label3.grid(row=4,column=1, columnspan=2, sticky=Tkinter.W)

            if pnixWeight == "Default":
                label4 = Tkinter.Entry(toplevel, width=100)
                label4.insert(0, "phenix.real_space_refine CA.rebuilt.pdb current.mrc resolution=5.0")
                label4.grid(row=5,column=1, columnspan=2, sticky=Tkinter.W)

            else:
                label4 = Tkinter.Entry(toplevel, width=100)
                label4.insert(0, "phenix.real_space_refine CA.rebuilt.pdb current.mrc resolution=" + pnixWeight)
                label4.grid(row=5,column=1, columnspan=2, sticky=Tkinter.W)

            label6 = Label(toplevel, text="                                                                            ", height=0)
            label6.grid(row=6,column=1, columnspan=2, sticky=Tkinter.W)



        #   this callback is called when the user clicked the "show result graph"
        #   in phenix refinement section. It will dispaly the Phenix refined CA model.
        def show_pnix_callback():
            global fileCount
            global MSTAE
            outfilePath = WorkPath.showWorkingPath()
            end = outfilePath.find('/MainMastUI')
            outfilePath = outfilePath[0:int(end)]
            prevdir = os.getcwd()
            newdir = outfilePath + "/MAINMAST/MAINMASTfile"

            global CAcreated_check

            check_CA_created()

            if not CAcreated_check:
                return
            
            try:
                os.chdir(newdir)
                rc("close all")
                fn = "CA.rebuilt.pdb"
                modelCArebuilt=chimera.openModels.open(fn)
                fn = "CA.rebuilt_real_space_refined.pdb"
                modelCArefine=chimera.openModels.open(fn)
                rc("display")
                MSTAE = 0
            except (IOError ,ZeroDivisionError),e:
                os.chdir(newdir)
                rc("close all")
                MSTAE = 0
            finally:
                os.chdir(prevdir)



        class ToggledFrame(Tkinter.Frame):

            def __init__(self, parent, text="", *args, **options):
                Tkinter.Frame.__init__(self, parent, *args, **options)

                self.show = Tkinter.IntVar()
                self.show.set(0)

                self.title_frame = ttk.Frame(self)
                self.title_frame.pack(fill="x", expand=1)

                ttk.Label(self.title_frame, text=text, width = 39).pack(side="left", fill="x", expand=1)

                self.toggle_button = ttk.Checkbutton(self.title_frame, width=2, text='+', command=self.toggle,
                                                    variable=self.show, style='Toolbutton')
                self.toggle_button.pack(side="left")

                self.sub_frame = Tkinter.Frame(self, relief="sunken", borderwidth=1)

            def toggle(self):
                if bool(self.show.get()):
                    self.sub_frame.pack(fill="x", expand=1)
                    self.toggle_button.configure(text='-')
                else:
                    self.sub_frame.forget()
                    self.toggle_button.configure(text='+')



        createFileUI = ToggledFrame(parent, text='Create MAINAMST files', relief="raised")
        createFileUI.grid(row=0,column=0, columnspan=2)
        displayGraphUI = ToggledFrame(parent, text='Display MAINAMST graphs', relief="raised")
        displayGraphUI.grid(row=1,column=0, columnspan=2)
        saveFileUI = ToggledFrame(parent, text='Save and Restore files', relief="raised")
        saveFileUI.grid(row=2,column=0, columnspan=3)



        #   The following code are for the GUI of MAINMAST plugin. 
        #   They specified the placement of bottons and input boxes.
        #   They also connects all the botton with the callback functions
        #   from above.

        rc("background solid white")
        Tkinter.Frame(createFileUI.sub_frame, width=390, height=580, padx=3, pady=3).grid(row=0, column =0, rowspan = 16, columnspan=2)
        Tkinter.Frame(displayGraphUI.sub_frame, bg='gray96', width=390, height=620, padx=3, pady=3).grid(row=0, column =0, rowspan = 16, columnspan=2)
        Tkinter.Frame(saveFileUI.sub_frame, width=390, height=158, padx=3, pady=3).grid(row=0, column =0, rowspan = 16, columnspan=3)
        MST_Button = Tkinter.Button(displayGraphUI.sub_frame, text=MSTree, highlightbackground='gray96', wraplength=80, width=10, height=3, command=MST_callback)

        MST_Button.grid(row=4, column=0, rowspan=2, sticky=Tkinter.W)

        AE_Button = Tkinter.Button(displayGraphUI.sub_frame, text=AllEdges, highlightbackground='gray96', wraplength=80, width=10, height=3, command=AE_callback)

        AE_Button.grid(row=6,column=0, rowspan=2, sticky=Tkinter.W)

        MCP_Button = Tkinter.Button(displayGraphUI.sub_frame, text=MCPath, highlightbackground='gray96', wraplength=80, width=10, height=3, command=MCP_callback)

        MCP_Button.grid(row=4, column=0, rowspan=2, sticky=Tkinter.E)

        CA_Button = Tkinter.Button(displayGraphUI.sub_frame, text=CAModel, highlightbackground='gray96', wraplength=80, width=10, height=3, command=CA_callback)

        CA_Button.grid(row=6,column=0, rowspan=2, sticky=Tkinter.E)


        pulchra_Button = Tkinter.Button(displayGraphUI.sub_frame, text=pulchra, highlightbackground='gray96', wraplength=80, width=10, height=3, command=pulchra_callback)

        pulchra_Button.grid(row=4,column=1, rowspan=2)

        ModelPanel_Button = Tkinter.Button(displayGraphUI.sub_frame, text=ModelPanel, highlightbackground='gray96', wraplength=80, width=10, height=1, command=ModelPanel_callback)

        ModelPanel_Button.grid(row=9,column=0, sticky=Tkinter.W)

        Map_Button = Tkinter.Button(displayGraphUI.sub_frame, text="Map file", highlightbackground='gray96', wraplength=80, width=9, height=1, command=Map_callback)

        Map_Button.grid(row=9,column=0, sticky=Tkinter.E)

        Map_Button = Tkinter.Button(displayGraphUI.sub_frame, text="Hide Map", highlightbackground='gray96', wraplength=80, width=10, height=1, command=Hide_Map_callback)

        Map_Button.grid(row=9,column=1)

        Save_Button = Tkinter.Button(saveFileUI.sub_frame, text="compare session&files", wraplength=80, width=10, height=6, command=store_file_before_compare)
        Save_Button.grid(row=1,column=2, rowspan=2)

        Save_Button = Tkinter.Button(saveFileUI.sub_frame, text="save session&files", wraplength=80, width=10, height=6, command=Save_callback)
        Save_Button.grid(row=1,column=0, rowspan=2)

        Restore_Button = Tkinter.Button(saveFileUI.sub_frame, text="restore session&file", wraplength=80, width=10, height=6, command=store_file_before_restore)

        Restore_Button.grid(row=1,column=1, rowspan=2)

        Tkinter.Label(createFileUI.sub_frame, text="Step 1: Files and attribute values for MainMast Execution").grid(row=0, column=0, columnspan=2, sticky=Tkinter.W)
        Tkinter.Label(displayGraphUI.sub_frame, text="Step 2: Click buttons for graph display", bg='gray96').grid(row=0, column=0, columnspan=2, sticky=Tkinter.W)
        Tkinter.Label(displayGraphUI.sub_frame, text="Click buttons to view MAINMAST output graph:", bg='gray96').grid(row=3, column=0, columnspan=2, sticky=Tkinter.W)
        Tkinter.Label(displayGraphUI.sub_frame, text="Supplement graphs:", bg='gray96').grid(row=8, column=0, columnspan=2, sticky=Tkinter.W)
        Tkinter.Label(saveFileUI.sub_frame, text="Save, Restore and Compare graphs:").grid(row=0, column=0, columnspan=3, sticky=Tkinter.W)
        Tkinter.Label(createFileUI.sub_frame, text="MainMast excuting progress:").grid(row=12, column=0, columnspan=2, sticky=Tkinter.W)
        Tkinter.Label(displayGraphUI.sub_frame, text="Run Phenix refinement:", bg='gray96').grid(row=10, column=0, columnspan=3, sticky=Tkinter.W)
        MSTcreate = Tkinter.Label(createFileUI.sub_frame, text="MST & all Edges: file not created")
        MSTcreate.grid(row=13, column=0, columnspan=2, sticky=Tkinter.W)

        #   this part in no longer use because the creation indicate has change from 4 rows to 2 rows.
        CAcreate = Tkinter.Label(createFileUI.sub_frame, text="All Files: file not created")
        CAcreate.grid(row=14, column=0, columnspan=2, sticky=Tkinter.W)
        # CAcreate = Tkinter.Label(createFileUI.sub_frame, text="All Files: ready to display")
        # CAcreate.grid(row=14, column=0, columnspan=2, sticky=Tkinter.W)

        Tkinter.Label(createFileUI.sub_frame, text="MAP file (situs format):").grid(row=1, column=0)
        efilePath = Tkinter.Entry(createFileUI.sub_frame)
        efileName = Tkinter.Entry(createFileUI.sub_frame)
        efileName.grid(row=1, column=1)
        file_Button = Tkinter.Button(createFileUI.sub_frame, text="select file", height=1, command=chooseFile_callback)

        Tkinter.Label(createFileUI.sub_frame, text="spd3 file:").grid(row=3, column=0)
        spd3filePath = Tkinter.Entry(createFileUI.sub_frame)
        spd3fileName = Tkinter.Entry(createFileUI.sub_frame)
        spd3fileName.grid(row=3, column=1)
        spd3file_Button = Tkinter.Button(createFileUI.sub_frame, text="select file", height=1, command=chooseSpd3File_callback)

        #   This part is no longer in use because we allow user to choose where to store
        #   the file in "save session&file" window.
        # Tkinter.Label(parent, text="Output file directory").grid(row=3, column=2)
        # ofilePath = Tkinter.Entry(parent)
        # prevdir = os.getcwd()
        # # newdir = prevdir + "/MAINMAST/MAINMASTfile"
        # # newdir = prevdir + "Users/yuhongzha/Desktop/MAINMASTplugin/MAINMAST/MAINMASTfile"
        # ofilePath.insert(0, prevdir)
        # ofilePath.grid(row=3, column=3)
        # outFile_Button = Tkinter.Button(parent, text="select directory", command=chooseOutFile_callback)

        Tkinter.Label(createFileUI.sub_frame, text="Threshold of density values:").grid(row=5, column=0)
        et = Tkinter.Entry(createFileUI.sub_frame)
        et.insert(0, t)

        Tkinter.Label(createFileUI.sub_frame, text="Filter of representative points:").grid(row=6, column=0)
        ePfilter = Tkinter.Entry(createFileUI.sub_frame)
        ePfilter.insert(0, Pfilter)

        Tkinter.Label(createFileUI.sub_frame, text="Maximum Edge distance:").grid(row=7, column=0)
        eDkeep = Tkinter.Entry(createFileUI.sub_frame)
        eDkeep.insert(0, Dkeep)

        Tkinter.Label(createFileUI.sub_frame, text="Size of tabu-list:").grid(row=8, column=0)
        eNtb = Tkinter.Entry(createFileUI.sub_frame)
        eNtb.insert(0, Ntb)

        Tkinter.Label(createFileUI.sub_frame, text="Radius of Local MST:").grid(row=9, column=0)
        eRlocal = Tkinter.Entry(createFileUI.sub_frame)
        eRlocal.insert(0, Rlocal)

        Tkinter.Label(createFileUI.sub_frame, text="Number of Iterations:").grid(row=10, column=0)
        eNround = Tkinter.Entry(createFileUI.sub_frame)
        eNround.insert(0, Nround)
        Tkinter.Label(displayGraphUI.sub_frame, text="Number of Main-chain Path shown:", bg='gray96').grid(row=1, column=0)
        MCP_Variable = Tkinter.StringVar(displayGraphUI.sub_frame)
        MCP_Variable.set("1")
        eNum_MCP = Tkinter.OptionMenu(displayGraphUI.sub_frame, MCP_Variable, "1", "2", "3", "4", "5", "6", "7", "8", "9", "10")
        eNum_MCP.config(width=len("kilograms"), bg='gray96')
        eNum_MCP.grid(row=1, column=1)


        Tkinter.Label(displayGraphUI.sub_frame, text="Number of CA file shown:", bg='gray96').grid(row=2, column=0)
        CA_Variable = Tkinter.StringVar(displayGraphUI.sub_frame)
        CA_Variable.set("1")
        eNum_CA = Tkinter.OptionMenu(displayGraphUI.sub_frame, CA_Variable, "1", "2", "3", "4", "5", "6", "7", "8", "9", "10")
        eNum_CA.config(width=len("kilograms"), bg='gray96')
        eNum_CA.grid(row=2, column=1)

        
        file_Button.grid(row=2, column=1)
        spd3file_Button.grid(row=4, column=1)
        et.grid(row=5, column=1)
        ePfilter.grid(row=6, column=1)
        eDkeep.grid(row=7, column=1)
        eNtb.grid(row=8, column=1)
        eRlocal.grid(row=9, column=1)
        eNround.grid(row=10, column=1)

        changeAttri_Button = Tkinter.Button(createFileUI.sub_frame, text="Create MST & All Edges", width=18, height=1, command=store_file_before_next_create)
        changeAttri_Button.grid(row=11,column=0, columnspan=2, sticky=Tkinter.W)

        changeAttri_Button = Tkinter.Button(createFileUI.sub_frame, text="Create all files", width=18, height=1, command=store_file_before_next_create_CA)
        changeAttri_Button.grid(row=11,column=0, columnspan=2, sticky=Tkinter.E)

        Tkinter.Label(displayGraphUI.sub_frame, text="Phenix refinement resolution:", bg='gray96').grid(row=11, column=0)
        pnix = Tkinter.Entry(displayGraphUI.sub_frame, bg='gray96', width = 10)
        pnix.insert(0, pnixW)
        pnix.grid(row=11, column=1)

        Tkinter.Label(displayGraphUI.sub_frame, text="mrc file for refinement:", bg='gray96').grid(row=12, column=0)
        pnix_mrc = Tkinter.Entry(displayGraphUI.sub_frame, bg='gray96', width = 10)
        pnix_mrc.grid(row=12, column=1)

        mrc_botton = Tkinter.Button(displayGraphUI.sub_frame, highlightbackground='gray96', text="select file", command=chooseMrcFile_callback)
        mrc_botton.grid(row = 13,column=1)


        pnixW_Button = Tkinter.Button(displayGraphUI.sub_frame, highlightbackground='gray96', text="Refinement command", width=18, height=1, command=pnixW_callback)
        pnixW_Button.grid(row=14,column=0, columnspan=2, sticky=Tkinter.W)

        pnix_Button = Tkinter.Button(displayGraphUI.sub_frame, highlightbackground='gray96', text="show result graph", width=18, height=1, command=show_pnix_callback)
        pnix_Button.grid(row=14,column=1, columnspan=2, sticky=Tkinter.W)

        print("current platform " + platform)



#   Now we register the above dialog with Chimera, so that it may be 
#   invoked via the 'display(name)' method of the chimera.dialogs module.
#   Here the class itself is registered, but since it is a named dialog
#   deriving from ModalDialog/ModelessDialog, the instance will automatically
#   reregister itself when first created.  This allows the 'dialogs.find()'
#   function to return the instance instead of the class.
chimera.dialogs.register(MainchainDialog.name, MainchainDialog)

#    Create the Chimera toolbar button that displays the dialog when
#    pressed.  Note that since the package is not normally searched for
#    icons, we have to prepend the path of this package to the icon's
#    file name.
dir, file = os.path.split(__file__)
icon = os.path.join(dir, 'MAINMASTlogo.tiff')
chimera.tkgui.app.toolbar.add(icon, lambda d=chimera.dialogs.display, n=MainchainDialog.name: d(n), 'MAINMAST', None)

