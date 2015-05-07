#!/bin/bash
python ./search.py
python ./preProcess.py
python ./reconcile.py -r ./rxnorm.pickle.bz2 -j ./officialImmList.txt ./out1/
python ./postProcess1.py
cat userImmList.txt > userPlusOfficalList.txt 
printf "\n" >> userPlusOfficalList.txt 
cat outRec1.txt >> userPlusOfficalList.txt
python ./reconcile.py -r ./rxnorm.pickle.bz2 -j ./userPlusOfficalList.txt ./FINAL_OUTPUT/
python ./postProcess2.py
cat FUZZY1.txt >> FINAL_FUZZY_DATES.txt
printf "\n Reconciled fuzzy dates are in ./FINAL_FUZZY_DATES.txt"
printf "\n Final Reconciled list is in ./FINAL_RECONCILE.txt \n"