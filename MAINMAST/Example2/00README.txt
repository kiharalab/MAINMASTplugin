#Tree
../MAINMAST -t 1.00 -filte 0.3 -Rlocal 10 -Tree -m 6374.situs > tree.pdb &
#Grapgh
../MAINMAST -t 1.00 -filte 0.3 -Rlocal 10 -Graph -m 6374.situs > graph.pdb &
#Main-chain trace
../MAINMAST -t 1.00 -filte 0.3 -Rlocal 10 -m 6374.situs > path.pdb &

#Secondary Structure Prediction by run_local.sh (SPIDER2)
run_local.sh 6374.seq


#Threading
../ThreadCA -i path.pdb -a ../20AA.param -spd 6374.spd3 -fw 1.4 -Ab 3.4 -Wb 0.9 > CA.pdb
../ThreadCA -i path.pdb -a ../20AA.param -spd 6374.spd3 -fw 1.4 -Ab 3.4 -Wb 0.9 -r > CA_r.pdb

#Visualize in pymol
../bondtree.pl tree.pdb > tmp
pymol -u tmp
../bondtree.pl graph.pdb > tmp
pymol -u tmp
../bondmk.pl CA.pdb > tmp
pymol -u tmp
../bondmk.pl CA_r.pdb > tmp
pymol -u tmp

