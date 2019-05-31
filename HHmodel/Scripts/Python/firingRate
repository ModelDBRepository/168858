#!/usr/bin/python

from lib import NeuronDirectory
from lib import NEURONInterface
from lib import ParameterSets
from lib.Paths import Paths

from optparse import OptionParser

import os
import sys

# Computes the firing rates, for a range of currents from ?? to ??, for the
# neuron named in its argument.  It assumes that the environment variable
# SIMULATION_PROJECT is defined, pointing to the paper project directory, which
# includes the Scripts/, EmpiricalData/ and NumericalResults/ directories.

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
parser.add_option("--headersWithConductances", action="store_true",
                  dest="headersWithConductancesOption",
                  default=False,
                  help="Prints the CSV-formatted headers for results")
parser.add_option("--appliedCurrent", action="store", type="string",
                  help=("Total current to apply to the neuron's soma, " +
                        "distributed between the holding current and the " +
                        "'stim' current.  Units are in nA."))
parser.add_option("--gNa", action="store", type="string",
                  help="Maximal sodium conductance")
parser.add_option("--gKv", action="store", type="string",
                  help="Maximal potassium conductance")
(options, args) = parser.parse_args()
headersOption = options.headersOption
headersWithConductancesOption = options.headersWithConductancesOption
parameterSetName = options.params
appliedCurrent = options.appliedCurrent
gNa = options.gNa
gKv = options.gKv
if (headersOption):
  print ("cellName,parameterSet,stim,firingRate")
  exit(0)
if (headersWithConductancesOption):
  print ("cellName,parameterSet,stim,gNa,gKv,firingRate")
  exit(0)
if (len(args) == 0):
  print 'Error: a neuron must be specified.'
  exit(1)
if (appliedCurrent == None):
  print 'Error: --appliedCurrent parameter must be specified.'
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

# NEURON uses nA for IClamp; we generally use pA
kPicoToNanoMultiplier = 0.001

firingRate = simulator.GetFiringRateForNeuron(
    neuron, float(appliedCurrent) * kPicoToNanoMultiplier, gNa, gKv)

if gNa is None or gKv is None:
  print "%s,%s,%s,%s" % (neuronName, parameterSetName, appliedCurrent, firingRate)
else:
  print "%s,%s,%s,%s,%s,%s" % (neuronName, parameterSetName, appliedCurrent,
                               gNa, gKv, firingRate)

