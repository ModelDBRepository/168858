#!/usr/bin/python

from lib import NeuronDirectory
from lib import ParameterSets

from optparse import OptionParser

import os
import sys

# Lists all the files described in the project's directory of neuron models, which is expected to be
# at ModelFiles/FileDirectory.csv.  It assumes that the environment variable SIMULATION_PROJECT is
# defined, pointing to the paper project directory, which includes the Scripts/, EmpiricalData/ and
# NumericalResults/ directories. If an argument is specified, it must be a space-delimited list of
# strings, each of which must be one of 'old-apical', 'young-apical', 'old-basal', 'young-basal',
# 'partial', 'whole', or the name of a neuron.  The script will then only list neurons that fall
# into those subsets.

parser = OptionParser()
parser.add_option("--params", action="store", type="string",
                  default="Christina-standard-testing",
                  help=("Name of the set of parameters that will be used in " +
                        "NEURON simulations supporting this computation, as " +
                        "specified in Scripts/ParameterSets.csv"))
(options, args) = parser.parse_args()
parameterSetName = options.params

parameterSets = ParameterSets.ParameterSets()
parameterSets.Load()
parameterSet = parameterSets.parameterSetForName(parameterSetName)
directory = NeuronDirectory.NeuronDirectory(parameterSet)
directory.Load()
neurons = []

argumentNames = sys.argv[1:]

if len(argumentNames) is 0:
  names = directory.Names()
  for each_name in names:
    print each_name
else:
  print "cellName,ageCategory"
  namesWithoutCommas = []
  for eachName in argumentNames:
    namesWithoutCommas.extend(eachName.split(","))
#   print namesWithoutCommas
  names = directory.ExpandNeuronNames(namesWithoutCommas)
  for eachName in names:
    neuron = directory.NeuronWithName(eachName)
    print "%s,%s" % (eachName, neuron.Age())

