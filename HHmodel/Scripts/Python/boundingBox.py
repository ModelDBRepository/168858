#!/usr/bin/python

from lib import NeuronDirectory
from lib import NEURONInterface
from lib.Paths import Paths
import lib.calcMeanBAP as calcMeanBAP

import os
import sys

# Computes the attenuation values L_out and L_in for the neuron named in its
# argument.  It assumes that the environment variable SIMULATION_PROJECT is
# defined, pointing to the paper project directory, which includes the Scripts/,
# EmpiricalData/ and NumericalResults/ directories.

###### Begin standard bootstrap code #######
# TODO(pcoskren): If this is consistent enough, you should be able to factor it
# out over all the Python computation commands.
directory = NeuronDirectory.NeuronDirectory()
directory.Load()

if len(sys.argv) < 2:
  print 'Error: a neuron must be specified.'
  exit(1)
neuron_name = sys.argv[1]
if neuron_name == "--headers":
  print ("name,xMin,yMin,zMin,xMax,yMax,zMax")
  exit(0)

neuron = directory.NeuronWithName(neuron_name)
neuron.Load()
neuron.SetHocRoot(Paths.hocFilesPath())

###### End standard header #######

box = neuron.BoundingBox()
print '%s,%f,%f,%f,%f,%f,%f' % (neuron.Name(), box[0][0], box[0][1], box[0][2],
    box[1][0], box[1][1], box[1][2])
