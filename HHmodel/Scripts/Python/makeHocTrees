#!/usr/bin/python

from lib import NeuronDirectory
from lib import NEURONInterface
from lib import ParameterSets
from lib.Paths import Paths

from optparse import OptionParser

import os
import sys

# Computes the a hoc file for the neuron named in its argument.  It assumes that
# the environment variable SIMULATION_PROJECT is defined, pointing to the paper
# project directory, which includes the Scripts/, EmpiricalData/ and
# NumericalResults/ directories.  The hoc file is written to the Scripts/Hoc/
# project directory.

###### Begin standard bootstrap code #######
# TODO(pcoskren): If this is consistent enough, you should be able to factor it
# out over all the Python computation commands.

parser = OptionParser()
parser.add_option("--params", action="store", type="string",
                  default="Christina-standard-testing",
                  help=("Name of the set of parameters that will be used in " +
                        "NEURON simulations supporting this computation, as " +
                        "specified in Scripts/ParameterSets.csv"))
(options, args) = parser.parse_args()
parameterSetName = options.params

if len(args) < 1:
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

###### End standard header #######

neuron.ConvertToHocFile(True, neuron.RootNode().Radius() * 0.25)

