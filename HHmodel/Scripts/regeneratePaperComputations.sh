#!/bin/bash
# This script assumes it's being run from the top-level project directory.

#export PARAMSET="Christina-standard-testing"
export PARAMSET="HHmodel-Point2"

# TODO: Bracket this with a flag.  It's a little too dangerous to always do it
# by default.
# echo "Deleting numerical results from previous run."
# rm NumericalResults/*csv
# rm HocFiles/*.hoc

echo "Generating hoc files for neurons"
./Scripts/Python/generateComputationCommands --params ${PARAMSET} \
   makeHoc:partial / \
   makeHocTrees:whole \
       | parallel --eta;

########## MBPAP, whole and partial, spiny and nonspiny ##########

#echo "Computing mbpap"

#./Scripts/Python/mbpap --headers > NumericalResults/mbpap-partial-spiny.csv
#./Scripts/Python/generateComputationCommands --params ${PARAMSET} \
#    mbpap:partial | parallel --eta \
#    >> NumericalResults/mbpap-partial-spiny.csv;

#./Scripts/Python/mbpap --headers > NumericalResults/mbpap-whole-spiny.csv
#./Scripts/Python/generateComputationCommands --params ${PARAMSET} mbpap:whole \
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

#echo "Computing attenuation"

#./Scripts/Python/attenuation --headers \
#    > NumericalResults/attenuation-partial-spiny.csv
#./Scripts/Python/generateComputationCommands --params ${PARAMSET} \
#    attenuation:partial | parallel --eta \
#    >> NumericalResults/attenuation-partial-spiny.csv;

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

#echo "Computing firing rates"

#./Scripts/Python/firingRate --headers > NumericalResults/firingRates_HH2.csv
#./Scripts/Python/generateComputationCommands --params ${PARAMSET} \
#    firingRate:whole:appliedCurrent=130 / \
#    firingRate:whole:appliedCurrent=230 / \
#   firingRate:whole:appliedCurrent=330 \
#    | parallel --eta \
#    >> NumericalResults/firingRates_HH2.csv


#./Scripts/Python/firingRate --headers > NumericalResults/firingRates.csv
#./Scripts/Python/generateComputationCommands --params ${PARAMSET} \
#    firingRate:whole:appliedCurrent=130 / \
#    firingRate:whole:appliedCurrent=180 / \
#    firingRate:whole:appliedCurrent=230 / \
#   firingRate:whole:appliedCurrent=280 / \
#   firingRate:whole:appliedCurrent=330 / \
#   firingRate:whole:appliedCurrent=380 \
#    | parallel --eta \
#    >> NumericalResults/firingRates.csv

########## Parameter space simulations

echo "Computing parameter spaces"

./Scripts/Python/generateParameterSpaceCommands --headers \
    > NumericalResults/parameterSpace_InFig5.csv
./Scripts/Python/generateParameterSpaceCommands --params ${PARAMSET} \
    --gNa=10,200 --gKv=10,200 --stepSize=5 --stims=230,330 \
    --neurons=Aug3f-all,Aug3g-all,Dec15e-all,Feb27n-all,Jun7d-all,May3t-all \
    | parallel --eta >> NumericalResults/parameterSpace_InFig5.csv

./Scripts/Python/generateParameterSpaceCommands --headers \
    > NumericalResults/parameterSpace_notInFig5.csv
./Scripts/Python/generateParameterSpaceCommands --params ${PARAMSET} \
    --gNa=10,200 --gKv=10,200 --stepSize=5 --stims=230,330 \
    --neurons=Aug3a-all,Aug3c-all,Aug3e-all,May3d-all,May3h-all,May3i-all \
    | parallel --eta >> NumericalResults/parameterSpace_notInFig5.csv

#./Scripts/Python/generateParameterSpaceCommands --headers \
#    > NumericalResults/parameterSpace.csv
#./Scripts/Python/generateParameterSpaceCommands --params ${PARAMSET} \
#    --gNa=10,200 --gKv=10,200 --stepSize=5 --stims=230,330 \
#    --neurons=Aug3a-all,Aug3c-all,Aug3e-all,Aug3f-all,Aug3g-all,Dec15e-all,Feb27n-all,Jun7d-all,May3d-all,May3h-all,May3i-all,May3j-all,May3t-all \
#    | parallel --eta >> NumericalResults/parameterSpace.csv


echo `date` > NumericalResults/lastRunTime.txt;
