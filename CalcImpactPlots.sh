#!bin/bash
masses=(1900)
#models=("WZ" "BulkWW" "BulkZZ" "ZprimeWW")
category=("WWHP") #"WWLP" "ZZHP" "ZZLP" "VVnew")
models=("BulkWW")
#category=("qVnew")

for mass in ${masses[@]}
do
    for model in ${models[@]}
    do 
        for c in ${category[@]}
        do
        #mass=1400
        #model="WZ"
        #cat="WZLP"
        datacard="datacards/CMS_jj_${model}_${mass}_13TeV_CMS_jj_${c}.txt"
        workspace="datacards/CMS_jj_${model}_${mass}_13TeV_CMS_jj_${c}.root"

        text2workspace.py $datacard -m $mass

        combineTool.py -M Impacts -d $workspace -m $mass --doInitialFit --robustFit 1

        combineTool.py -M Impacts -d $workspace -m $mass --robustFit 1 --doFits

        combineTool.py -M Impacts -d $workspace -m $mass -o impacts.json

        plotImpacts.py -i impacts.json -o impacts

        mv ./impacts.pdf Impacts_${model}_${mass}_${c}.pdf
        done
    done
done

