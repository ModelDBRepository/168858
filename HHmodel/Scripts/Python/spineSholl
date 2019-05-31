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
  print ("cellName,parameterSet,radius,spineCount,sectionLength,spineDensity")
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

shollData = neuron.SpineSholl3D(20, 10)
for eachRadiusData in shollData:
  print '%s,%s,%d,%d,%f,%f' % (eachRadiusData["name"], parameterSetName,
                              eachRadiusData["radius"],
                              eachRadiusData["spineCount"],
                              eachRadiusData["sectionLength"],
                              (eachRadiusData["spineCount"] /
                                  eachRadiusData["sectionLength"]))
