#!/usr/bin/python

from lib import NeuronDirectory
from lib import NEURONInterface
from lib import ParameterSets
from lib.Paths import Paths
import lib.calcMeanBAP as calcMeanBAP

from optparse import OptionParser

import os
import sys

# Computes the attenuation values L_out and L_in for the neuron named in its
# argument.  It assumes that the environment variable SIMULATION_PROJECT is
# defined, pointing to the paper project directory, which includes the Scripts/,
# EmpiricalData/ and NumericalResults/ directories.

###### Begin standard bootstrap code #######
# TODO(pcoskren): If this is consistent enough, you should be able to factor it
# out over all the Python computation commands.
parser = OptionParser()
parser.add_option("--params", action="store", type="string",
                  default="Christina-standard-testing",
                  help=("Name of the set of parameters that will be used in " +
                        "NEURON simulations supporting this computation, as " +
                        "specified in Scripts/ParameterSets.csv"))
parser.add_option("--headers", action="store_true", dest="headersOption", default=False,
                  help="Prints the CSV-formatted headers for results")
(options, args) = parser.parse_args()
headersOption = options.headersOption
parameterSetName = options.params
if (headersOption):
  print ("cellName,parameterSet,radius,numberIntersections,intersectionArea,meanIntersectionDiameter")
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

###### End standard header #######

sholl_data = neuron.Sholl3d(20)
for each_tuple in sholl_data:
  tupleWithParameterName = (parameterSetName, each_tuple[0], each_tuple[1],
                            each_tuple[2], each_tuple[3])
  print neuron.Name() + ",%s,%f,%f,%f,%f" % tupleWithParameterName
