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

echo "Computing parameter spaces"

./Scripts/Python/generateParameterSpaceCommands --headers \
    > NumericalResults/parameterSpace_aug3a.csv
./Scripts/Python/generateParameterSpaceCommands --params "customPass-aug3a" \
    --gNa=10,200 --gKv=10,200 --stepSize=5 --stims=230,330 \
    --neurons=Aug3a-all \
    | parallel --eta >> NumericalResults/parameterSpace_aug3a.csv


./Scripts/Python/generateParameterSpaceCommands --headers \
    > NumericalResults/parameterSpace_aug3c.csv
./Scripts/Python/generateParameterSpaceCommands --params "customPass-aug3c" \
    --gNa=10,200 --gKv=10,200 --stepSize=5 --stims=230,330 \
    --neurons=Aug3c-all \
    | parallel --eta >> NumericalResults/parameterSpace_aug3c.csv


./Scripts/Python/generateParameterSpaceCommands --headers \
    > NumericalResults/parameterSpace_aug3e.csv
./Scripts/Python/generateParameterSpaceCommands --params "customPass-aug3e" \
    --gNa=10,200 --gKv=10,200 --stepSize=5 --stims=230,330 \
    --neurons=Aug3e-all \
    | parallel --eta >> NumericalResults/parameterSpace_aug3e.csv


./Scripts/Python/generateParameterSpaceCommands --headers \
    > NumericalResults/parameterSpace_aug3f.csv
./Scripts/Python/generateParameterSpaceCommands --params "customPass-aug3f" \
    --gNa=10,200 --gKv=10,200 --stepSize=5 --stims=230,330 \
    --neurons=Aug3f-all \
    | parallel --eta >> NumericalResults/parameterSpace_aug3f.csv


./Scripts/Python/generateParameterSpaceCommands --headers \
    > NumericalResults/parameterSpace_aug3g.csv
./Scripts/Python/generateParameterSpaceCommands --params "customPass-aug3g" \
    --gNa=10,200 --gKv=10,200 --stepSize=5 --stims=230,330 \
    --neurons=Aug3g-all \
    | parallel --eta >> NumericalResults/parameterSpace_aug3g.csv


./Scripts/Python/generateParameterSpaceCommands --headers \
    > NumericalResults/parameterSpace_feb27n.csv
./Scripts/Python/generateParameterSpaceCommands --params "customPass-feb27n" \
    --gNa=10,200 --gKv=10,200 --stepSize=5 --stims=230,330 \
    --neurons=Feb27n-all \
    | parallel --eta >> NumericalResults/parameterSpace_feb27n.csv


./Scripts/Python/generateParameterSpaceCommands --headers \
    > NumericalResults/parameterSpace_dec15e.csv
./Scripts/Python/generateParameterSpaceCommands --params "customPass-dec15e" \
    --gNa=10,200 --gKv=10,200 --stepSize=5 --stims=230,330 \
    --neurons=Dec15e-all \
    | parallel --eta >> NumericalResults/parameterSpace_dec15e.csv


./Scripts/Python/generateParameterSpaceCommands --headers \
    > NumericalResults/parameterSpace_jun7d.csv
./Scripts/Python/generateParameterSpaceCommands --params "customPass-jun7d" \
    --gNa=10,200 --gKv=10,200 --stepSize=5 --stims=230,330 \
    --neurons=Jun7d-all \
    | parallel --eta >> NumericalResults/parameterSpace_jun7d.csv


./Scripts/Python/generateParameterSpaceCommands --headers \
    > NumericalResults/parameterSpace_may3d.csv
./Scripts/Python/generateParameterSpaceCommands --params "customPass-may3d" \
    --gNa=10,200 --gKv=10,200 --stepSize=5 --stims=230,330 \
    --neurons=May3d-all \
    | parallel --eta >> NumericalResults/parameterSpace_may3d.csv


./Scripts/Python/generateParameterSpaceCommands --headers \
    > NumericalResults/parameterSpace_may3h.csv
./Scripts/Python/generateParameterSpaceCommands --params "customPass-may3h" \
    --gNa=10,200 --gKv=10,200 --stepSize=5 --stims=230,330 \
    --neurons=May3h-all \
    | parallel --eta >> NumericalResults/parameterSpace_may3h.csv


./Scripts/Python/generateParameterSpaceCommands --headers \
    > NumericalResults/parameterSpace_may3i.csv
./Scripts/Python/generateParameterSpaceCommands --params "customPass-may3i" \
    --gNa=10,200 --gKv=10,200 --stepSize=5 --stims=230,330 \
    --neurons=May3i-all \
    | parallel --eta >> NumericalResults/parameterSpace_may3i.csv


./Scripts/Python/generateParameterSpaceCommands --headers \
    > NumericalResults/parameterSpace_may3t.csv
./Scripts/Python/generateParameterSpaceCommands --params "customPass-may3t" \
    --gNa=10,200 --gKv=10,200 --stepSize=5 --stims=230,330 \
    --neurons=May3t-all \
    | parallel --eta >> NumericalResults/parameterSpace_may3t.csv


#echo `date` > NumericalResults/lastRunTime.txt;
