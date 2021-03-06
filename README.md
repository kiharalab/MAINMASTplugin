#  MAINMAST plugin for Chimera
Last Updated: 06/30/2019

### Licence
(c) 2019 Yuhong Zha, Genki Terashi, Daisuke Kihara and Purdue University 

MAINMAST is the free software for academic and non-commercial users.
It is released under the terms of the GNU General Public License Ver.3 (https://www.gnu.org/licenses/gpl-3.0.en.html).
Commercial users please contact dkihara@purdue.edu for alternate licensing.

Citation of the following reference should be included in any publication that uses data or results generated by MAINMAST program.

[(a) Terashi, G., & Kihara, D. (2018). De novo main-chain modeling for EM maps using MAINMAST. Nature communications, 9(1), 1618.](https://www.nature.com/articles/s41467-018-04053-7)

## Introduction

MAINMAST is short for MAINchain Model trAcing using Spanning Tree from a EM map. It directly traces main-chain connections and C-alpha positions by using Tree-Graph models on the EM map. Reference: [Terashi, G., & Kihara, D. (2018). De novo main-chain modeling for EM maps using MAINMAST. Nature communications, 9(1), 1618.](https://www.nature.com/articles/s41467-018-04053-7)

MAINMAST is a de novo modeling method for EM maps of near atomic resolution (less than ~4.5 angstrom).

To view more information about MAINMAST, please visit [MAINMAST website](http://kiharalab.org/mainmast/index.html).

__If you encounter any problem using the plugin, please contact zha0@purdue.edu (zha-zero) or gterashi@purdue.edu.__

## Getting Started

This part will guide you through the process of installation:
1. Install Chimera.
2. Required packages.
3. Download the MAINMAST plugin.
4. Set up plugin configurations.

__Note: The current version is for Linux and Mac only.__

#### Install Chimera

MAINMAST plugin is a ready to run tool working on the Chimera. To use MAINMAST plugin, please first download and install the [UCSF Chimera](https://www.cgl.ucsf.edu/chimera/download.html).
After downloaded Chimera, follow the instruction on Chimera website to finish installation.

#### Before installation

MAINMAST plugin takes both file in `.situs` format and corresponding `.spd3` file to generate output file. So make sure you have both `.situs` format and corresponding `.spd3` file. If not, we have provided example files for you to try.

In order to achieve the full functionality of the MAINMAST plugin, you should have the following package installed: 

__PULCHRA__: PULCHRA reconstructs full-atom model from MAINMAST C-alpha models.
More information can be find [here](http://www.pirx.com/pulchra/).
```
pulchra CA_model.pdb
```

__PHENIX refinement__: General purpose crystallographic structure refinement program. More information can be find [here](https://www.phenix-online.org/documentation/reference/refinement.html) and [here](https://www.phenix-online.org/documentation/reference/real_space_refine.html)
```
phenix.real_space_refine model.pdb map.ccp4 resolution=4.2
```

(you can still use MAINMAST plugin if the following package is not installed, but you will not be able to use the PULCHRA reconstruction and PHENIX refinement function)

#### Download MAINMAST plugin

Download plugin code from Github [here](https://github.com/kiharalab/MAINMASTplugin.git). 

###### This first step is really important!!! 
Make sure you remember the path where you put this file, it will be used for set up configuration later. 

For example, if the file is stored at
```
/user/Desktop/MAINMASTplugin
```
Then __your_path_to_MAINMASTplugin__ will be
```
/user/Desktop
```
#### Set up plugin configurations

##### First, set up plugin's working directory. 
To set up this configuration, go to WorkPath.py located at:
```
/your_path_to_MAINMASTplugin/MAINMASTplugin/MainMastUI/WorkPath.py
```
and change it to:
```
def showWorkingPath():
return "/your_path_to_MAINMASTplugin/MAINMASTplugin/MainMastUI"
```
Remember, __your_path_to_MAINMASTplugin__ is where you saved your MAINMASTplugin file and has to use  __absolute path__. 
(For example, 
__Use__ "/net/user/your_path_to_MAINMASTplugin/MAINMASTplugin/MainMastUI"; 
__Do not use__ "~/your_path_to_MAINMASTplugin/MAINMASTplugin/MainMastUI")

##### Second, build excutable file. 
Compile from source codes:
```
cd /your_path_to_MAINMASTplugin/MAINMAST
gfortran MAINMAST.f -O3 -fbounds-check -o MAINMAST -mcmodel=medium
gfortran ThreadCA.f -O3 -fbounds-check -o ThreadCA -mcmodel=medium
```
If you do not have gfortran, please install it first from here https://gcc.gnu.org/wiki/GFortranBinaries.

##### Third, add the plugin to Chimera. 
First, open Chimera. Find where you installed Chimera and open it.

Once the Chimera is open, you have to add MAINMASTplugin extension to Chimera program.

To do this, first got to Chimera  `Favorites`-> `Preferences...`-> `Tools`, then click `Add...`, then select the MAINMASTplugin folder you just selected and click `Close`. Finally, click `Save` to apply the change. REMEMBER: when select the MAINMASTplugin folder, only click the folder once. Do not select any of the child folders. For example, if the folder is located at "Desktop/MAINMASTplugin", you should see Third-party plugin locations showing "Desktop".

Finally, go to Chimera  `Tools`-> `General Controls`-> `IDLE`

Chimera will open a Python Shell window. In the command line, type

```
import MainMastUI.gui
```

If you see a button with MAINMAST logo appear on top left corner, then you are ready to use the program.

## Running MAINMAST plugin

<img src="https://github.com/kiharalab/MAINMASTplugin/blob/master/imgs/img1.png" width="330">

Click on the MAINMAST logo appeared in Chimera to launch the plugin. 
Basic components of MAINMAST plugin can be separated into 3 parts:

#### Section 1: Create MAINMAST files

<img src="https://github.com/kiharalab/MAINMASTplugin/blob/master/imgs/img2.png" width="240">

This is the beginning section of MAINMAST plugin: file creation. After upload all required files and set all attributes, plugin will create MAINMAST output file automatically. We will explain in detail of __required files__, __attribute value meanings__, __create file button functions__.

##### Required files

In order for the plugin to successfully create the output file, we need to upload a MAP file in `.situs` format and corresponding `.spd3` file.

You can use [this example](http://kiharalab.org/mainmast/Tutorials.html#ex1) to try first. This provided example includes a `1yfd.situs` and a `1yfd.spd3`

##### Attribute value meanings:
---Parameters in MeanShift---
`Threshold of density values`. default=0.0

--Parameters in Tabu-search---
`Filter of representative points`. default=0.1
`Maximum Edge distance`. Keep edge where distance < [f]. default=0.5
`Size of tabu-list`. default=100
`Radius of Local MST`. default=10
`Number of Iterations`
Note: All attribute values must be entered before generating graph. No field can be empty.

More detailed explanation of each attributes can be found [here](http://kiharalab.org/mainmast/Tutorials.html#mainmast).

##### Create file botton functions:

There are two button for user to choose: `Create MST & ALL Edges` and a `Create all files`

__Create MST & ALL Edges__: 
Only generate the Minimum Spanning tree file and all possible connections(edges) file on the EM map.
This process will identify local dense points in an EM map by Mean Shifting clustering algorithm and Connect all LDPs by Minimum Spanning Tree. It only takes a small amount of time, so it can be used to check if the Minimum Spanning tree works well in your input graph before generating other graphs.

__Create all files__: 
Generate all files, including Minimum Spanning tree file, all possible connections(edges) file, traced main-chain file, Threaded sequence(ThreadCA) file, and Pulchra rebuild model file.
This process will perform additional task of Refine Tree structure by Tabu Search algorithm and Thread sequence on the longest path. It will be performed based on the Minimum Spanning Tree generated before. 

Choose the button that suits your purpose the most. We recommend first used `Create MST & ALL Edges` to check the correctness of Minimum Spanning tree.   `Create all files` will be significantly slower than `Create MST & ALL Edges`, so you may want to make sure the Minimum Spanning tree is correct before generating all files.

When creating the file, the lower middle session of window will change the displaying words from "file not created" to "generating files", and the __window will be frozen during the time of file creation__. You will not be able to click any buttons during this period. After the displaying words change to "ready to display", you can continue using the window. Here shows an example after we click `Create MST & ALL Edges`:

Before click the button, the windows shows "MST & all Edges: file not created"

<img src="https://github.com/kiharalab/MAINMASTplugin/blob/master/imgs/img_file_not_created.png" width="240">

After click the button, the windows changes to "MST & all Edges: generating files" and becomes frozen

<img src="https://github.com/kiharalab/MAINMASTplugin/blob/master/imgs/img_generating.png" width="240">

When file creation finishes, the windows shows "MST & all Edges: ready to display"

<img src="https://github.com/kiharalab/MAINMASTplugin/blob/master/imgs/img_ready_to_display.png" width="240">

#### Section 2: Display MAINMAST graphs

<img src="https://github.com/kiharalab/MAINMASTplugin/blob/master/imgs/img2_new.png" width="240">

This is the file display section of MAINMAST plugin. In this section, you can change the number of Main-chain files and ThreadCA files shown using __Number of Main-chain Path shown__ and __Number of CA file shown__. You can also display all graph you created using buttons.

##### Click button for graph display:

`Number of Main-chain Path shown`: Number of all possible edges shown. There are in total 10 different all possible edges files created by MAINMAST. You can choose the number of files shown from 1 to 10. 
The default number of Main-chain Path shown is 1.

`Number of CA file shown`: Number of Threaded sequence(ThreadCA) shown. There are in total 10 different Threaded sequence(ThreadCA) files created by MAINMAST. You can choose the number of files shown from 1 to 10. 
The default number of CA Path shown is 1.

##### Click button to view MAINMAST output graph:

Those are the buttons that used to display the files created by MAINMAST, they are:

`Minimum Spanning Tree` displays a graph structure that connects all vertices with the minimum total length of edges.

`All Edges` displays all possible connections(edges) on the EM map

`Main-chain Path` displays further improved protein main-chain path. The initial tree structure (MST) is refined in an iterative procedure using a tabu search. A tabu search attempts to explore a large search space by keeping a list of moves that are forbidden.

`Predicted CA model` displays the result of thread sequence on the longest path. The longest path of a tree is aligned with the amino acid sequence using the Smith-Waterman Dynamic Programming algorithm.

`Pulchra Rebuild` displays the Predicted CA model and CA rebuilt model

##### Supplement graphs:

`Model Panel` opens the model panel for user to select, unselect, view or hide the current graphs

`Map file/Hide Map` display/hide the corresponding '.situs' file with transparency of 0.5

##### Run Phenix refinement:

Enter the phenix refinement resolution(default 5.0) and upload a .mrc format file corresponds to you input MAP file, then click __Refinement command__, the program will show you commands like this:

```
cd /your_path_to_MAINMASTplugin/MAINMASTplugin/MAINMAST/MAINMASTfile
module load phenix
phenix.real_space_refine CA.rebuilt.pdb current.mrc resolution=5.0
```

Copy those command line by line to your terminal. After success, go back to the plugin and click __show result graph__. It will show you the phenix refined graph.

#### Section 3: Save and restore files

<img src="https://github.com/kiharalab/MAINMASTplugin/blob/master/imgs/img4.png" width="240">

In this section, you can either save all files to your __own directory__ and restore them later.

__your own places__:
`save session&file`: Save the current files to directory you selected. It will also store the zoom in/out percentage and the orientation of the current display.
`restore session&file`: Restore the file from the directory you selected. It will restore the last displayed graph, the zoom in/out percentage and the orientation.
`compare session&file`: Select up to 3 files previously stored and compare their graphs. You can compare all output files stated in __section 2__.
<img src="https://github.com/kiharalab/MAINMASTplugin/blob/master/imgs/img5.png" width="330">


## Other useful resources

#### Chimera Programmer's site.

```
https://www.cgl.ucsf.edu/chimera/current/docs/ProgrammersGuide/index.html
https://www.cgl.ucsf.edu/chimera/current/docs/ProgrammersGuide/Examples/index.html
```

For example, we can see how to use command line programs (Blast, Modeller, etc) on Chimera.
```
https://www.cgl.ucsf.edu/chimera/current/docs/ProgrammersGuide/Examples/Main_RunSubprocess.html
```

#### About __MAINMAST__

Programs are available at
http://kiharalab.org/mainmast/

There are 2 examples:
http://kiharalab.org/mainmast/Tutorials.html#ex1

All files described before are located at
http://kiharalab.org/mainmast/Downloads.html


