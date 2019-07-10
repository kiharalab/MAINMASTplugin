#Generating Minimum Spanning Tree
../MAINMAST -m 1yfq.situs  -t 9 -filter 0.3 -Dkeep 1.0 -Ntb 10 -Rlocal 5 -Nlocal 50 -Nround 50 -Tree > tree.pdb &

#find all possible connections
../MAINMAST -m 1yfq.situs  -t 9 -filter 0.3 -Dkeep 1.0 -Ntb 10 -Rlocal 5 -Nlocal 50 -Nround 50 -Graph > graph.pdb &

#main-chain path tracing
../MAINMAST -m 1yfq.situs  -t 9 -filter 0.3 -Dkeep 1.0 -Ntb 10 -Rlocal 5 -Nlocal 50 -Nround 50 > path.pdb &

#Secondary Structure Prediction by run_local.sh (SPIDER2)
run_local.sh 1yfq.seq

#threading
../ThreadCA -i path.pdb -a ./20AA.param -spd 1yfq.spd3  -fw 1.3  -Ab 3.3 -Wb 0.9 >CA.pdb
../ThreadCA -i path.pdb -a ./20AA.param -spd 1yfq.spd3  -fw 1.3  -Ab 3.3 -Wb 0.9 -r >CA_r.pdb

#Visualize in pymol
../bondtree.pl tree.pdb > tmp
pymol -u tmp
../bondtree.pl graph.pdb > tmp
pymol -u tmp
../bondmk.pl CA.pdb > tmp
pymol -u tmp
../bondmk.pl CA_r.pdb > tmp
pymol -u tmp

