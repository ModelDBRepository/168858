#!/usr/bin/python

from lib import NeuronDirectory
from lib import NEURONInterface
from lib import ParameterSets
from lib.Paths import Paths

from optparse import OptionParser

import os
import sys

# Computes the input resistance for the neuron named in its argument.  It
# assumes that the environment variable SIMULATION_PROJECT is defined, pointing
# to the paper project directory, which includes the Scripts/, EmpiricalData/
# and NumericalResults/ directories.

###### Begin standard bootstrap code with spine support #######
# TODO(pcoskren): If this is consistent enough, you should be able to factor it
# out over all the Python computation commands that need run with or without spines
parser = OptionParser()
parser.add_option("--params", action="store", type="string",
                  default="Christina-standard-testing",
                  help=("Name of the set of parameters that will be used in " +
                        "NEURON simulations supporting this computation, as " +
                        "specified in Scripts/ParameterSets.csv"))
parser.add_option("--headers", action="store_true", dest="headersOption",
                  default=False,
                  help="Prints the CSV-formatted headers for results")
(options, args) = parser.parse_args()
headersOption = options.headersOption
parameterSetName = options.params
if (headersOption):
  print ("cellName,parameterSet,simRn")
  exit(0)
if (len(args) == 0):
  print 'Error: a neuron must be specified.'
  exit(1)
neuronName = args[0]

parameterSets = ParameterSets.ParameterSets()
parameterSets.Load()
parameterSet = parameterSets.parameterSetForName(parameterSetName)
directory = NeuronDirectory.NeuronDirectory(parameterSet)
directory.Load()
neuron = directory.NeuronWithName(neuronName)
neuron.Load()
neuron.SetHocRoot(Paths.hocFilesPath())

###### End standard bootstrap code with spine support #######

simulator = NEURONInterface.NEURONInterface(Paths.hocScriptsPath(), parameterSet)

inputResistance = simulator.GetRnForNeuron(neuron)
print("%s,%s,%f" % (neuronName, parameterSetName, inputResistance))
