#!/bin/bash
# This script assumes it's being run from the top-level project directory.

export PARAMSET="customPass-aug3a"

# TODO: Bracket this with a flag.  It's a little too dangerous to always do it
# by default.
# echo "Deleting numerical results from previous run."
# rm NumericalResults/*csv
# rm HocFiles/*.hoc

# ----------------> 8/22/14 by cmw:  skip all of this
#
echo "Generating hoc files for neurons"
./Scripts/Python/generateComputationCommands --params ${PARAMSET} \
   makeHoc:partial / \
  makeHocTrees:whole \
       | parallel --eta;

# here are the custom parameter sets:
#--params "customPass-aug3a" \
#./Scripts/Python/generateParameterSpaceCommands --params "customPass-aug3c" \
#./Scripts/Python/generateParameterSpaceCommands --params "customPass-aug3e" \
#./Scripts/Python/generateParameterSpaceCommands --params "customPass-aug3f" \
#/Scripts/Python/generateParameterSpaceCommands --params "customPass-aug3g" \
#/Scripts/Python/generateParameterSpaceCommands --params "customPass-feb27n" \
#./Scripts/Python/generateParameterSpaceCommands --params "customPass-dec15e" \
#./Scripts/Python/generateParameterSpaceCommands --params "customPass-jun7d" \
#/Scripts/Python/generateParameterSpaceCommands --params "customPass-may3d" \
#./Scripts/Python/generateParameterSpaceCommands --params "customPass-may3h" \
#./Scripts/Python/generateParameterSpaceCommands --params "customPass-may3i" \
#/Scripts/Python/generateParameterSpaceCommands --params "customPass-may3t" \

########## MBPAP, whole and partial, spiny and nonspiny ##########

#echo "Computing mbpap"

#./Scripts/Python/mbpap --headers > NumericalResults/mbpap-whole-spiny-aug3a.csv
#./Scripts/Python/generateComputationCommands --params "customPass-aug3a"  mbpap:whole \
#   | parallel --eta >> NumericalResults/mbpap-whole-spiny.csv;

#./Scripts/Python/mbpap --headers --nospines > NumericalResults/mbpap-partial-nospines.csv
#./Scripts/Python/generateComputationCommands --params ${PARAMSET} \
#    mbpap:partial:nospines | parallel --eta \
#    >> NumericalResults/mbpap-partial-nospines.csv;

#./Scripts/Python/mbpap --headers --nospines > NumericalResults/mbpap-whole-nospines.csv
#./Scripts/Python/generateComputationCommands --params ${PARAMSET} \
#    mbpap:whole:nospines | parallel --eta \
#    >> NumericalResults/mbpap-whole-nospines.csv;

########## attenuation, partial, spiny and nonspiny ##########

echo "Computing attenuation"

./Scripts/Python/attenuation --headers \
    > NumericalResults/attenuation-partial-spiny-aug3a.csv
./Scripts/Python/generateComputationCommands --params "customPass-aug3a" \
    attenuation:partial | parallel --eta \
    >> NumericalResults/attenuation-partial-spiny-aug3a.csv;
    
./Scripts/Python/attenuation --headers \
    > NumericalResults/attenuation-partial-spiny-aug3c.csv
./Scripts/Python/generateComputationCommands --params "customPass-aug3c" \
    attenuation:partial | parallel --eta \
    >> NumericalResults/attenuation-partial-spiny-aug3c.csv;
    
./Scripts/Python/attenuation --headers \
    > NumericalResults/attenuation-partial-spiny-aug3e.csv
./Scripts/Python/generateComputationCommands --params "customPass-aug3e" \
    attenuation:partial | parallel --eta \
    >> NumericalResults/attenuation-partial-spiny-aug3e.csv;
    
./Scripts/Python/attenuation --headers \
    > NumericalResults/attenuation-partial-spiny-aug3f.csv
./Scripts/Python/generateComputationCommands --params "customPass-aug3f" \
    attenuation:partial | parallel --eta \
    >> NumericalResults/attenuation-partial-spiny-aug3f.csv;
    
./Scripts/Python/attenuation --headers \
    > NumericalResults/attenuation-partial-spiny-aug3g.csv
./Scripts/Python/generateComputationCommands --params "customPass-aug3g" \
    attenuation:partial | parallel --eta \
    >> NumericalResults/attenuation-partial-spiny-aug3g.csv;
    
./Scripts/Python/attenuation --headers \
    > NumericalResults/attenuation-partial-spiny-feb27n.csv
./Scripts/Python/generateComputationCommands --params "customPass-feb27n" \
    attenuation:partial | parallel --eta \
    >> NumericalResults/attenuation-partial-spiny-feb27n.csv;
    
./Scripts/Python/attenuation --headers \
    > NumericalResults/attenuation-partial-spiny-dec15e.csv
./Scripts/Python/generateComputationCommands --params "customPass-dec15e" \
    attenuation:partial | parallel --eta \
    >> NumericalResults/attenuation-partial-spiny-dec15e.csv;
    
./Scripts/Python/attenuation --headers \
    > NumericalResults/attenuation-partial-spiny-jun7d.csv
./Scripts/Python/generateComputationCommands --params "customPass-jun7d" \
    attenuation:partial | parallel --eta \
    >> NumericalResults/attenuation-partial-spiny-jun7d.csv;
    
./Scripts/Python/attenuation --headers \
    > NumericalResults/attenuation-partial-spiny-may3d.csv
./Scripts/Python/generateComputationCommands --params "customPass-may3d" \
    attenuation:partial | parallel --eta \
    >> NumericalResults/attenuation-partial-spiny-may3d.csv;
    
./Scripts/Python/attenuation --headers \
    > NumericalResults/attenuation-partial-spiny-may3h.csv
./Scripts/Python/generateComputationCommands --params "customPass-may3h" \
    attenuation:partial | parallel --eta \
    >> NumericalResults/attenuation-partial-spiny-may3h.csv;
    
./Scripts/Python/attenuation --headers \
    > NumericalResults/attenuation-partial-spiny-may3i.csv
./Scripts/Python/generateComputationCommands --params "customPass-may3i" \
    attenuation:partial | parallel --eta \
    >> NumericalResults/attenuation-partial-spiny-may3i.csv;
            
./Scripts/Python/attenuation --headers \
    > NumericalResults/attenuation-partial-spiny-may3t.csv
./Scripts/Python/generateComputationCommands --params "customPass-may3t" \
    attenuation:partial | parallel --eta \
    >> NumericalResults/attenuation-partial-spiny-may3t.csv;

# here are the custom parameter sets:
#--params "customPass-may3t" \
#./Scripts/Python/generateParameterSpaceCommands --params "customPass-aug3c" \
#./Scripts/Python/generateParameterSpaceCommands --params "customPass-aug3e" \
#./Scripts/Python/generateParameterSpaceCommands --params "customPass-aug3f" \
#/Scripts/Python/generateParameterSpaceCommands --params "customPass-aug3g" \
#/Scripts/Python/generateParameterSpaceCommands --params "customPass-feb27n" \
#./Scripts/Python/generateParameterSpaceCommands --params "customPass-dec15e" \
#./Scripts/Python/generateParameterSpaceCommands --params "customPass-jun7d" \
#/Scripts/Python/generateParameterSpaceCommands --params "customPass-may3d" \
#./Scripts/Python/generateParameterSpaceCommands --params "customPass-may3h" \
#./Scripts/Python/generateParameterSpaceCommands --params "customPass-may3i" \
#/Scripts/Python/generateParameterSpaceCommands --params "customPass-may3t" \

#./Scripts/Python/attenuation --headers --nospines \
#    > NumericalResults/attenuation-partial-nospines.csv
#./Scripts/Python/generateComputationCommands --params ${PARAMSET} \
#    attenuation:partial:nospines | parallel --eta \
#    >> NumericalResults/attenuation-partial-nospines.csv;

########## geometry, partial ##########

#./Scripts/Python/geometry --headers > NumericalResults/geometry.csv
#./Scripts/Python/generateComputationCommands --params ${PARAMSET} \
#    geometry:partial | parallel --eta >> NumericalResults/geometry.csv;

########## sholl and spinesholl, partial

#echo "Computing Sholl measurements"

#./Scripts/Python/sholl --headers > NumericalResults/sholl.csv
#./Scripts/Python/generateComputationCommands --params ${PARAMSET} \
#    sholl:partial | parallel --eta >> NumericalResults/sholl.csv;

#./Scripts/Python/spinesholl --headers > NumericalResults/spinesholl.csv
#./Scripts/Python/generateComputationCommands --params ${PARAMSET} \
#    spinesholl:partial | parallel --eta >> NumericalResults/spinesholl.csv;

########## Rn and firing rate simulations

#echo "Computing input resistance"

#./Scripts/Python/inputResistance --headers > NumericalResults/inputResistance.csv
#./Scripts/Python/generateComputationCommands --params ${PARAMSET} \
#    inputResistance:whole | parallel --eta >> NumericalResults/inputResistance.csv;

#
# ----------------> 8/22/14 by cmw:  skip all of this


# ----------------> 8/22/14 by cmw:  just run simplified firing rate and parameter space commands

#echo "Computing firing rates"

# 8/22/14 by cmw:  minimal calculations - to find why parameter set is not read correctly

#./Scripts/Python/firingRate --headers > NumericalResults/firingRates_FRtest.csv
#./Scripts/Python/generateComputationCommands --params ${PARAMSET} \
#    firingRate:whole:appliedCurrent=330 \
#   | parallel --eta \
#    >> NumericalResults/firingRates_FRtest.csv


########## Parameter space simulations

#echo "Computing parameter spaces"

#./Scripts/Python/generateParameterSpaceCommands --headers \
#    > NumericalResults/parameterSpace_may3tP1.csv
#./Scripts/Python/generateParameterSpaceCommands --params "customPass-may3t" \
#    --gNa=60,160 --gKv=150,150 --stepSize=100 --stims=30,80,130,180,230,280,330 \
#    --neurons=May3t-all \
#    | parallel --eta >> NumericalResults/parameterSpace_may3tP1.csv


#echo `date` > NumericalResults/lastRunTime.txt;
