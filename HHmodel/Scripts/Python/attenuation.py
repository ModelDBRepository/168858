#!/usr/bin/python

from lib import NeuronDirectory
from lib import NEURONInterface
from lib import ParameterSets
from lib.Paths import Paths

from optparse import OptionParser

import os
import sys

# Computes the attenuation values L_out and L_in for the neuron named in its
# argument.  It assumes that the environment variable SIMULATION_PROJECT is
# defined, pointing to the paper project directory, which includes the Scripts/,
# EmpiricalData/ and NumericalResults/ directories.

###### Begin standard bootstrap code with spine support #######
# TODO(pcoskren): If this is consistent enough, you should be able to factor it
# out over all the Python computation commands that need run with or without spines
parser = OptionParser()
parser.add_option("--spines", action="store_true", dest="hasSpines",
                  default=True,
                  help=("Simulation will incorporate surface area of spines " +
                        "(but not simulate them explicitly)"))
parser.add_option("--nospines", action="store_false", dest="hasSpines",
                  help="If specified, any spines associated with the neuron " +
                       "will be ignored")
parser.add_option("--params", action="store", type="string",
                  default="Christina-standard-testing",
                  help=("Name of the set of parameters that will be used in " +
                        "NEURON simulations supporting this computation, as " +
                        "specified in Scripts/ParameterSets.csv"))
parser.add_option("--headers", action="store_true", dest="headersOption",
                  default=False,
                  help="Prints the CSV-formatted headers for results")
(options, args) = parser.parse_args()
hasSpines = options.hasSpines
headersOption = options.headersOption
parameterSetName = options.params
if (headersOption):
  if hasSpines:
    suffix = "spines"
  else:
    suffix = "nospines"

  headerTuples = zip(
      ["out"] * 6 + ["in"] * 6,
      range(0,501,100) * 2,
      [suffix] * 12)
  headerItems = ",".join(["%s.%dHz.%s" % x for x in headerTuples])
  print ("cellName,parameterSet," + headerItems)
  exit(0)

if (len(args) == 0):
  print 'Error: a neuron must be specified.'
  exit(1)
neuron_name = args[0]

parameterSets = ParameterSets.ParameterSets()
parameterSets.Load()
parameterSet = parameterSets.parameterSetForName(parameterSetName)
directory = NeuronDirectory.NeuronDirectory(parameterSet)
directory.Load()
neuron = directory.NeuronWithName(neuron_name)
neuron.Load()
neuron.SetHocRoot(Paths.hocFilesPath())

###### End standard bootstrap code with spine support #######

simulator = NEURONInterface.NEURONInterface(Paths.hocScriptsPath(), parameterSet)

spine_type = 0
if neuron.Arbor() == neuron.kApicalArbor:
  spine_type = simulator.kApicalSpines
elif neuron.Arbor() == neuron.kBasalArbor:
  spine_type = simulator.kBasalSpines
attenuations = simulator.GetAttenuationsForNeuron(neuron, spine_type, hasSpines)
print("%s,%s,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f" % (
    neuron.Name(),
    parameterSetName,
    attenuations.outward_attenuations_by_frequency[0],
    attenuations.outward_attenuations_by_frequency[100],
    attenuations.outward_attenuations_by_frequency[200],
    attenuations.outward_attenuations_by_frequency[300],
    attenuations.outward_attenuations_by_frequency[400],
    attenuations.outward_attenuations_by_frequency[500],
    attenuations.inward_attenuations_by_frequency[0],
    attenuations.inward_attenuations_by_frequency[100],
    attenuations.inward_attenuations_by_frequency[200],
    attenuations.inward_attenuations_by_frequency[300],
    attenuations.inward_attenuations_by_frequency[400],
    attenuations.inward_attenuations_by_frequency[500]))
