#!/usr/bin/python

from lib import NeuronDirectory
from lib import NEURONInterface
from lib import ParameterSets
from lib.Paths import Paths
import lib.calcMeanBAP as calcMeanBAP

from optparse import OptionParser

import os
import re
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
parser.add_option("--nospines", action="store_false", dest="hasSpines")
parser.add_option("--params", action="store", type="string",
                  default="Christina-standard-testing",
                  help=("Name of the set of parameters that will be used in " +
                        "NEURON simulations supporting this computation, as " +
                        "specified in Scripts/ParameterSets.csv"))
parser.add_option("--headers", action="store_true", dest="headersOption", default=False,
                  help="Prints the CSV-formatted headers for results")
(options, args) = parser.parse_args()
hasSpines = options.hasSpines
headersOption = options.headersOption
parameterSetName = options.params
if (headersOption):
  if hasSpines:
    print ("cellName,parameterSet,mBPAP.spines")
  else:
    print ("cellName,parameterSet,mBPAP.nospines")
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

spine_type = 0
NEURON = NEURONInterface.NEURONInterface(Paths.hocScriptsPath(), parameterSet)
if neuron.Arbor() == neuron.kCompleteArbor:
  apicalName = re.sub(r'-all',r'-apical',neuron_name)
  apicalNeuron = directory.NeuronWithName(apicalName)
  apicalNeuron.Load()
  apicalNeuron.SetHocRoot(Paths.hocFilesPath())
  basalName = re.sub(r'-all',r'-basal',neuron_name)
  basalNeuron = directory.NeuronWithName(basalName)
  basalNeuron.Load()
  basalNeuron.SetHocRoot(Paths.hocFilesPath())
  apicalData = NEURON.GetBPAPForNeuron(apicalNeuron, NEURON.kApicalSpines, hasSpines)
  basalData = NEURON.GetBPAPForNeuron(basalNeuron, NEURON.kBasalSpines, hasSpines)
  data = apicalData + basalData
else:
  if neuron.Arbor() == neuron.kApicalArbor:
    spine_type = NEURON.kApicalSpines
  elif neuron.Arbor() == neuron.kBasalArbor:
    spine_type = NEURON.kBasalSpines
  data = NEURON.GetBPAPForNeuron(neuron, spine_type, hasSpines)
mbpap = calcMeanBAP.ComputeNBPArea(data)
print "%s,%s,%f" % (neuron.Name(), parameterSetName, mbpap)
