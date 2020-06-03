# DijetCombineLimitCode

- Script to run all steps of the VBF VV resonance analysis:

`python runAllUHH_selectedMasses_cuts_newStrategy.py`

- Script to run all steps of the VBF VV aQGC analysis:

`python runAllUHH_aQGC.py`

- To install complete environment (assuming `/cvmfs` is mounted and you are running on `el7` )
```bash
wget https://raw.githubusercontent.com/stalbrec/DijetCombineLimitCode/aQGC_2020/scripts/install.sh
source install.sh
```
this will setup a `CMSSW_10_2_13` environment and install both combine and combineHarvester and clone this repo so you are ready to go.

