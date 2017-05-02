# DijetCombineLimitCode
Scripts for producing limits for all-hadronic VV and qV analyses

## F-test
Takes as input a .root file with 1 GeV binned histograms of dijet invariant mass (0-7000 GeV). Names of histograms are names of analysis category, eg. "DijetMassHighPuriWW"
For F-test in MC (set error to largest of MC and Poisson error)
```
python scripts/ftest_MC.py
```
For F-test in data SR 
```
python scripts/ftest_SR_qstar.py //qV analysis
python scripts/ftest_SR.py //VV analysis
same files can also be used to do the sideband fits in data
```
Remember to change input file! And name of out .tex file!

## Do likelihood fits:
Plot likelihood fits after F-test outcome is ready using chosen fit function. Same input as above.
```
python scripts/sb-fit-bkgonly_qstar.py  //qV analysis
python scripts/sb-fit-bkgonly.py  //VV analysis
```

## Produce workspaces:
To interpolate signal MC, take as input .root files of signal MC.  with 1 GeV binned histograms of dijet invariant mass (0-7000 GeV). Names of histograms are names of analysis category, eg. "DijetMassHighPuriWW". Attention: here you should use rootfiles with lumiweights applied and not scaled to the dataluminosity. This scaling is done in the workspace generation so it would be double if we did it here also!
These scripts are designed to run on the PSI T3 batch system (qsub protocol)! Needs adaption to run on alternate systems.
Modify interpolateAll.py to signal sample and masspoints you wish to run on
```
python interpolateAll.py -> if you want to do them manually do: python interpolateVV13TeV.py input/ZprimeWW_13TeV_ 2100 GeV
-> in this file the names of the used histograms have to be adjusted to qV <-> VV etc. !
```
Create data and signal MC minitrees
```
root -l MiniTreeProducerVV13TeV.C
root -l MiniTreeSignalProducerqV13TeV.C //qV analysis
root -l MiniTreeSignalProducerVV13TeV.C //VV analysis
```
Produce workspaces and datacards. Remember to change which signals and masspoints you wanna run over! Need to be available as minitrees!
```
when changing parameters of fit functions change them here: BkgModelFitBernstein
and also here:  MakeBkgWS
and also change the paramters written as nuisance in the datacard here:  MakeDataCard_1Channel
python ProduceWorkspaces13TeV.py
```
Implement JES/JER/JMS/JMR  and cross section uncertanties
```
python implement-JESJMRsystematics.py
python implement-XsecUncertainty.py
python implement-tau21PtUnc.py
```
## Run limits:
To run limits you need to have datacards and workspaces produced as instructed above. 
To combine mass category and purities
```
python Limits/CombineDatacards.py 
```
To run limits (also here, adjusted to T3 batch system!!)
```
python Limits/CalcAsympLimits.py
```
To draw brasilian flag
```
cd Limits
python brazilianFlag.py
```
To calculate and draw p-values (not yet adjusted for batch system! Run locally (fast). Work in progress!)
```
cd ..
python Limits/CalcPvalue.py
python Limits/CalcPvalue.py
python Limits/CalcPvalueStep2.py
cd Limits
python pValuePlots.py
```
