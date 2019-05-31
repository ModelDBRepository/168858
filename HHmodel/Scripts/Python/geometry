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
#
# Data is output in CSV format, without a header so that results from multiple
# invocations can be easily combined.  The columns are:
# name
# volume
# surface area
# total length
# number of sections
# mean section length
# spine count
# spine volume
# spine surface area
# spine density
#
# If the argument is "--headers", then the column headers are printed in CSV
# format.  The specified neuron, if any, is ignored.

###### Begin standard bootstrap code #######
# TODO(pcoskren): If this is consistent enough, you should be able to factor it
# out over all the Python computation commands.

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
  print ("cellName,parameterSet,volume,surfaceArea,totalLength,"
         "numberOfSections,meanSectionLength,spineCount,spineVolume,"
         "spineSurfaceArea,spineDensity")
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

(spineVolume, spineArea) = neuron.SpineVolumeAndArea()

print "%s,%s,%f,%f,%f,%f,%f,%f,%f,%f,%f" % (
  neuron.Name(),
  parameterSetName,
  neuron.Volume(),
  neuron.SurfaceArea(),
  neuron.CumulativeLength(),
  neuron.DendriteSectionCount(),
  neuron.MeanSectionLength(),
  neuron.SpineCount(),
  spineVolume,
  spineArea,
  neuron.SpineDensity())
