#!bin/bash
#selections=("tau21" "tau21_deta4" "tau21_deta5" "tau21_deta6" "tau21_04" "tau21_04_deta4" "tau21_04_deta5" "tau21_04_deta6" "tau21_05" "tau21_05_deta4" "tau21_05_deta5" "tau21_05_deta6" "tau21_06" "tau21_06_deta4" "tau21_06_deta5" "tau21_06_deta6" "tau21_07" "tau21_07_deta4" "tau21_07_deta5" "tau21_07_deta6")
selections=("VV" "VBF" "invM500" "invM1000" "invM1500" "invM2000" "invM2500" "invM3000" "invM3500" "invM4000")
echo ${#selections[@]}
selNumber=${#selections[@]}
echo $selNumber
#dir=CHS
#dir=pt30etaAK4
dir=mjjVBFSelHigh
echo $dir
#for i in {0..$selNumber}
mkdir input/$dir/
for ((i=0;i<$selNumber;i+=1))
do
    echo ${selections[$i]}
    echo root -b -q "PrepareRootFile.C(\"${selections[$i]}\")"
    root -b -q "PrepareRootFile.C(\"${selections[$i]}\",\"$dir\")" 
done
for ((i=0;i<$selNumber;i+=1))
do
    cp -p input/graviton_${selections[$i]}_1200.root  input/$dir/
    cp -p input/graviton_${selections[$i]}_1400.root  input/$dir/
    cp -p input/graviton_${selections[$i]}_1600.root  input/$dir/
    cp -p input/graviton_${selections[$i]}_1800.root  input/$dir/
    cp -p input/graviton_${selections[$i]}_2000.root  input/$dir/
    cp -p input/graviton_${selections[$i]}_2500.root  input/$dir/
    cp -p input/graviton_${selections[$i]}_3000.root  input/$dir/
    cp -p input/graviton_${selections[$i]}_3500.root  input/$dir/
    cp -p input/graviton_${selections[$i]}_4000.root  input/$dir/
    cp -p input/graviton_${selections[$i]}_4500.root  input/$dir/
    cp -p input/radion_${selections[$i]}_1200.root  input/$dir/
    cp -p input/radion_${selections[$i]}_1400.root  input/$dir/
    cp -p input/radion_${selections[$i]}_1600.root  input/$dir/
    cp -p input/radion_${selections[$i]}_1800.root  input/$dir/
    cp -p input/radion_${selections[$i]}_2000.root  input/$dir/
    cp -p input/radion_${selections[$i]}_2500.root  input/$dir/
    cp -p input/radion_${selections[$i]}_3000.root  input/$dir/
    cp -p input/radion_${selections[$i]}_3500.root  input/$dir/
    cp -p input/radion_${selections[$i]}_4000.root  input/$dir/
    cp -p input/radion_${selections[$i]}_4500.root  input/$dir/
done
python runAllUHH_selectedMasses_cuts_newStrategy.py

for ((i=0;i<$selNumber;i+=1))
do
    cp -p input/graviton_${selections[$i]}_Interpolated1200.root input/$dir/
    cp -p input/graviton_${selections[$i]}_Interpolated2000.root input/$dir/
    cp -p input/graviton_${selections[$i]}_Interpolated4000.root input/$dir/
    cp -p input/radion_${selections[$i]}_Interpolated1200.root input/$dir/
    cp -p input/radion_${selections[$i]}_Interpolated2000.root input/$dir/
    cp -p input/radion_${selections[$i]}_Interpolated4000.root input/$dir/

    rm input/graviton_${selections[$i]}_1200.root   
    rm input/graviton_${selections[$i]}_1400.root   
    rm input/graviton_${selections[$i]}_1600.root   
    rm input/graviton_${selections[$i]}_1800.root   
    rm input/graviton_${selections[$i]}_2000.root   
    rm input/graviton_${selections[$i]}_2500.root   
    rm input/graviton_${selections[$i]}_3000.root   
    rm input/graviton_${selections[$i]}_3500.root   
    rm input/graviton_${selections[$i]}_4000.root   
    rm input/graviton_${selections[$i]}_4500.root   
    rm input/radion_${selections[$i]}_1200.root   
    rm input/radion_${selections[$i]}_1400.root   
    rm input/radion_${selections[$i]}_1600.root   
    rm input/radion_${selections[$i]}_1800.root   
    rm input/radion_${selections[$i]}_2000.root   
    rm input/radion_${selections[$i]}_2500.root   
    rm input/radion_${selections[$i]}_3000.root   
    rm input/radion_${selections[$i]}_3500.root   
    rm input/radion_${selections[$i]}_4000.root   
    rm input/radion_${selections[$i]}_4500.root   
done
mkdir workspaces/$dir/
mkdir datacards/$dir/
mkdir plots/$dir/
mkdir LimitTxt/$dir/
mkdir Limits/$dir/
for ((i=0;i<$selNumber;i+=1))
do
    cp -p workspaces/CMS_jj_graviton_${selections[$i]}_1200_13TeV.root workspaces/$dir/
    cp -p workspaces/CMS_jj_graviton_${selections[$i]}_2000_13TeV.root workspaces/$dir/
    cp -p workspaces/CMS_jj_graviton_${selections[$i]}_4000_13TeV.root workspaces/$dir/
    cp -p workspaces/CMS_jj_radion_${selections[$i]}_1200_13TeV.root workspaces/$dir/
    cp -p workspaces/CMS_jj_radion_${selections[$i]}_2000_13TeV.root workspaces/$dir/
    cp -p workspaces/CMS_jj_radion_${selections[$i]}_4000_13TeV.root workspaces/$dir/
    cp -p workspaces/CMS_jj_bkg_VV_${selections[$i]}_1200_13TeV.root workspaces/$dir/
    cp -p workspaces/CMS_jj_bkg_VV_${selections[$i]}_2000_13TeV.root workspaces/$dir/
    cp -p workspaces/CMS_jj_bkg_VV_${selections[$i]}_4000_13TeV.root workspaces/$dir/
    cp -p datacards/CMS_jj_graviton_${selections[$i]}_1200_13TeV__invMass_limit1_submit.src datacards/$dir/
    cp -p datacards/CMS_jj_graviton_${selections[$i]}_1200_13TeV__invMass_afterVBFsel_limit1_submit.src datacards/$dir/
    cp -p datacards/CMS_jj_graviton_${selections[$i]}_2000_13TeV__invMass_limit1_submit.src datacards/$dir/
    cp -p datacards/CMS_jj_graviton_${selections[$i]}_2000_13TeV__invMass_afterVBFsel_limit1_submit.src datacards/$dir/
    cp -p datacards/CMS_jj_graviton_${selections[$i]}_4000_13TeV__invMass_limit1_submit.src datacards/$dir/
    cp -p datacards/CMS_jj_graviton_${selections[$i]}_4000_13TeV__invMass_afterVBFsel_limit1_submit.src datacards/$dir/
    cp -p datacards/CMS_jj_radion_${selections[$i]}_1200_13TeV__invMass_limit1_submit.src datacards/$dir/
    cp -p datacards/CMS_jj_radion_${selections[$i]}_1200_13TeV__invMass_afterVBFsel_limit1_submit.src datacards/$dir/
    cp -p datacards/CMS_jj_radion_${selections[$i]}_2000_13TeV__invMass_limit1_submit.src datacards/$dir/
    cp -p datacards/CMS_jj_radion_${selections[$i]}_2000_13TeV__invMass_afterVBFsel_limit1_submit.src datacards/$dir/
    cp -p datacards/CMS_jj_radion_${selections[$i]}_4000_13TeV__invMass_limit1_submit.src datacards/$dir/
    cp -p datacards/CMS_jj_radion_${selections[$i]}_4000_13TeV__invMass_afterVBFsel_limit1_submit.src datacards/$dir/

    cp -p datacards/CMS_jj_graviton_${selections[$i]}_1200_13TeV__invMass.txt datacards/$dir/
    cp -p datacards/CMS_jj_graviton_${selections[$i]}_1200_13TeV__invMass_afterVBFsel.txt datacards/$dir/
    cp -p datacards/CMS_jj_graviton_${selections[$i]}_2000_13TeV__invMass.txt datacards/$dir/
    cp -p datacards/CMS_jj_graviton_${selections[$i]}_2000_13TeV__invMass_afterVBFsel.txt datacards/$dir/
    cp -p datacards/CMS_jj_graviton_${selections[$i]}_4000_13TeV__invMass.txt datacards/$dir/
    cp -p datacards/CMS_jj_graviton_${selections[$i]}_4000_13TeV__invMass_afterVBFsel.txt datacards/$dir/
    cp -p datacards/CMS_jj_radion_${selections[$i]}_1200_13TeV__invMass.txt datacards/$dir/
    cp -p datacards/CMS_jj_radion_${selections[$i]}_1200_13TeV__invMass_afterVBFsel.txt datacards/$dir/
    cp -p datacards/CMS_jj_radion_${selections[$i]}_2000_13TeV__invMass.txt datacards/$dir/
    cp -p datacards/CMS_jj_radion_${selections[$i]}_2000_13TeV__invMass_afterVBFsel.txt datacards/$dir/
    cp -p datacards/CMS_jj_radion_${selections[$i]}_4000_13TeV__invMass.txt datacards/$dir/
    cp -p datacards/CMS_jj_radion_${selections[$i]}_4000_13TeV__invMass_afterVBFsel.txt datacards/$dir/

    cp -p plots/sigmodel_graviton_${selections[$i]}1200__invMass*.* plots/$dir/
    cp -p plots/sigmodel_graviton_${selections[$i]}2000__invMass*.* plots/$dir/
    cp -p plots/sigmodel_graviton_${selections[$i]}4000__invMass*.* plots/$dir/
    cp -p plots/fitDiagnosticsgraviton${selections[$i]}1200_invMass*.root plots/$dir/
    cp -p plots/fitDiagnosticsgraviton${selections[$i]}2000_invMass*.root plots/$dir/
    cp -p plots/fitDiagnosticsgraviton${selections[$i]}4000_invMass*.root plots/$dir/
    cp -p plots/sigmodel_radion_${selections[$i]}1200__invMass*.* plots/$dir/
    cp -p plots/sigmodel_radion_${selections[$i]}2000__invMass*.* plots/$dir/
    cp -p plots/sigmodel_radion_${selections[$i]}4000__invMass*.* plots/$dir/
    cp -p plots/fitDiagnosticsradion${selections[$i]}1200_invMass*.root plots/$dir/
    cp -p plots/fitDiagnosticsradion${selections[$i]}2000_invMass*.root plots/$dir/
    cp -p plots/fitDiagnosticsradion${selections[$i]}4000_invMass*.root plots/$dir/
    cp -p LimitTxt/graviton__invMass_${selections[$i]}_new_combined_Limit.txt LimitTxt/$dir/
    cp -p LimitTxt/graviton__invMass_afterVBFsel_${selections[$i]}_new_combined_Limit.txt LimitTxt/$dir/
    cp -p LimitTxt/radion__invMass_${selections[$i]}_new_combined_Limit.txt LimitTxt/$dir/
    cp -p LimitTxt/radion__invMass_afterVBFsel_${selections[$i]}_new_combined_Limit.txt LimitTxt/$dir/
    cp -p Limits/brazilianFlag_graviton__invMass_${selections[$i]}_new_combined_13TeV.* Limits/$dir/
    cp -p Limits/brazilianFlag_graviton__invMass_afterVBFsel_${selections[$i]}_new_combined_13TeV.* Limits/$dir/
    cp -p Limits/brazilianFlag_radion__invMass_${selections[$i]}_new_combined_13TeV.* Limits/$dir/
    cp -p Limits/brazilianFlag_radion__invMass_afterVBFsel_${selections[$i]}_new_combined_13TeV.* Limits/$dir/

    rm input/graviton_${selections[$i]}_Interpolated1200.root  
    rm input/graviton_${selections[$i]}_Interpolated2000.root  
    rm input/graviton_${selections[$i]}_Interpolated4000.root  
    rm input/radion_${selections[$i]}_Interpolated1200.root  
    rm input/radion_${selections[$i]}_Interpolated2000.root  
    rm input/radion_${selections[$i]}_Interpolated4000.root  

    rm workspaces/CMS_jj_graviton_${selections[$i]}_1200_13TeV.root 
    rm workspaces/CMS_jj_graviton_${selections[$i]}_2000_13TeV.root 
    rm workspaces/CMS_jj_graviton_${selections[$i]}_4000_13TeV.root 
    rm workspaces/CMS_jj_radion_${selections[$i]}_1200_13TeV.root 
    rm workspaces/CMS_jj_radion_${selections[$i]}_2000_13TeV.root 
    rm workspaces/CMS_jj_radion_${selections[$i]}_4000_13TeV.root 
    rm workspaces/CMS_jj_bkg_VV_${selections[$i]}_1200_13TeV.root 
    rm workspaces/CMS_jj_bkg_VV_${selections[$i]}_2000_13TeV.root 
    rm workspaces/CMS_jj_bkg_VV_${selections[$i]}_4000_13TeV.root 
    rm datacards/CMS_jj_graviton_${selections[$i]}_1200_13TeV__invMass_limit1_submit.src 
    rm datacards/CMS_jj_graviton_${selections[$i]}_1200_13TeV__invMass_afterVBFsel_limit1_submit.src
    rm datacards/CMS_jj_graviton_${selections[$i]}_2000_13TeV__invMass_limit1_submit.src 
    rm datacards/CMS_jj_graviton_${selections[$i]}_2000_13TeV__invMass_afterVBFsel_limit1_submit.src 
    rm datacards/CMS_jj_graviton_${selections[$i]}_4000_13TeV__invMass_limit1_submit.src 
    rm datacards/CMS_jj_graviton_${selections[$i]}_4000_13TeV__invMass_afterVBFsel_limit1_submit.src 
    rm datacards/CMS_jj_radion_${selections[$i]}_1200_13TeV__invMass_limit1_submit.src 
    rm datacards/CMS_jj_radion_${selections[$i]}_1200_13TeV__invMass_afterVBFsel_limit1_submit.src 
    rm datacards/CMS_jj_radion_${selections[$i]}_2000_13TeV__invMass_limit1_submit.src 
    rm datacards/CMS_jj_radion_${selections[$i]}_2000_13TeV__invMass_afterVBFsel_limit1_submit.src 
    rm datacards/CMS_jj_radion_${selections[$i]}_4000_13TeV__invMass_limit1_submit.src 
    rm datacards/CMS_jj_radion_${selections[$i]}_4000_13TeV__invMass_afterVBFsel_limit1_submit.src 
    rm datacards/CMS_jj_graviton_${selections[$i]}_1200_13TeV__invMass.txt 
    rm datacards/CMS_jj_graviton_${selections[$i]}_1200_13TeV__invMass_afterVBFsel.txt
    rm datacards/CMS_jj_graviton_${selections[$i]}_2000_13TeV__invMass.txt
    rm datacards/CMS_jj_graviton_${selections[$i]}_2000_13TeV__invMass_afterVBFsel.txt
    rm datacards/CMS_jj_graviton_${selections[$i]}_4000_13TeV__invMass.txt
    rm datacards/CMS_jj_graviton_${selections[$i]}_4000_13TeV__invMass_afterVBFsel.txt
    rm datacards/CMS_jj_radion_${selections[$i]}_1200_13TeV__invMass.txt
    rm datacards/CMS_jj_radion_${selections[$i]}_1200_13TeV__invMass_afterVBFsel.txt
    rm datacards/CMS_jj_radion_${selections[$i]}_2000_13TeV__invMass.txt
    rm datacards/CMS_jj_radion_${selections[$i]}_2000_13TeV__invMass_afterVBFsel.txt
    rm datacards/CMS_jj_radion_${selections[$i]}_4000_13TeV__invMass.txt
    rm datacards/CMS_jj_radion_${selections[$i]}_4000_13TeV__invMass_afterVBFsel.txt 
    rm plots/sigmodel_graviton_${selections[$i]}1200__invMass*.* 
    rm plots/sigmodel_graviton_${selections[$i]}2000__invMass*.* 
    rm plots/sigmodel_graviton_${selections[$i]}4000__invMass*.* 
    rm plots/fitDiagnosticsgraviton${selections[$i]}1200_invMass*.root 
    rm plots/fitDiagnosticsgraviton${selections[$i]}2000_invMass*.root 
    rm plots/fitDiagnosticsgraviton${selections[$i]}4000_invMass*.root 
    rm plots/sigmodel_radion_${selections[$i]}1200__invMass*.* 
    rm plots/sigmodel_radion_${selections[$i]}2000__invMass*.* 
    rm plots/sigmodel_radion_${selections[$i]}4000__invMass*.* 
    rm plots/fitDiagnosticsradion${selections[$i]}1200_invMass*.root 
    rm plots/fitDiagnosticsradion${selections[$i]}2000_invMass*.root 
    rm plots/fitDiagnosticsradion${selections[$i]}4000_invMass*.root 
    rm LimitTxt/graviton__invMass_${selections[$i]}_new_combined_Limit.txt 
    rm LimitTxt/graviton__invMass_afterVBFsel_${selections[$i]}_new_combined_Limit.txt 
    rm LimitTxt/radion__invMass_${selections[$i]}_new_combined_Limit.txt 
    rm LimitTxt/radion__invMass_afterVBFsel_${selections[$i]}_new_combined_Limit.txt 
    rm Limits/brazilianFlag_graviton__invMass_${selections[$i]}_new_combined_13TeV.* 
    rm Limits/brazilianFlag_graviton__invMass_afterVBFsel_${selections[$i]}_new_combined_13TeV.* 
    rm Limits/brazilianFlag_radion__invMass_${selections[$i]}_new_combined_13TeV.* 
    rm Limits/brazilianFlag_radion__invMass_afterVBFsel_${selections[$i]}_new_combined_13TeV.* 
done
