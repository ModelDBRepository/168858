#!/usr/bin/python

from optparse import OptionParser

# Generates a series of commands that, in aggregate, produce a parameter space
# of neuron firing rates, where the parameters that vary are maximim sodium
# conductance (gNa) and maximum potassium conductance (gKv).  Each is specified
# by an argument consisting of the minumum and maximum parameter value,
# separated by a comma.  The --stepsize parameter specifies the amount by which
# each parameter is varied.  The --stims parameter is a comma-separated list of
# the different stimulation levels that should be applied to the simulated
# neuron.  The --neurons argument is a comma-separated list of the neurons
# for which a map should be generated.  Neurons can be specified by any name (or
# group name) recognized by the 'list.py' script.
#
# Example:
# Scripts/Python/generateParameterSpaceCommands --params=testing --gNa=0,200 --gKv=0,200 \
#   --stepSize=5 --stims=230,330 --neurons=Aug3a-all,Aug3b-all

parser = OptionParser()
parser.add_option("--headers", action="store_true", dest="headersOption",
                  default=False,
                  help="Prints the CSV-formatted headers for results")
parser.add_option("--params", action="store", type="string",
                  default="Christina-standard-testing",
                  help=("Name of the set of parameters that will be used in " +
                        "NEURON simulations supporting this computation, as " +
                        "specified in Scripts/ParameterSets.csv"))
parser.add_option("--gNa", action="store", type="string",
                  help="Maximal sodium conductance.  Must be an integer.")
parser.add_option("--gKv", action="store", type="string",
                  help="Maximal potassium conductance.  Must be an integer.")
parser.add_option("--stepSize", action="store", type="string",
                  help="amount by which the parameters vary.  Must be an integer.")
parser.add_option("--stims", action="store", type="string",
                  help="levels of current (pA) to be applied to each neuron")
parser.add_option("--neurons", action="store", type="string",
                  help="neurons for which a parameter space should be computed")
(options, args) = parser.parse_args()
headersOption = options.headersOption
if (headersOption):
  print ("cellName,parameterSet,gNa,gKv,stim,firingRate")
  exit(0)
parameterSetName = options.params
gNaParam = options.gNa
gKvParam = options.gKv
stepSize = int(options.stepSize)
stimsParam = options.stims
neuronsParam = options.neurons

gNaLevels = gNaParam.split(",")
gNaLow = int(gNaLevels[0])
gNaHigh = int(gNaLevels[1])

gKvLevels = gKvParam.split(",")
gKvLow = int(gKvLevels[0])
gKvHigh = int(gKvLevels[1])

stims = [float(x) for x in stimsParam.split(",")]
neuronNames = neuronsParam.split(",")

def commandForNaKvStim(gNa, gKv, stim, neuronName):
  return ("./Scripts/Python/firingRate.py --appliedCurrent=330 " +
          "--params=%s --gNa=%d --gKv=%d --appliedCurrent=%d %s") % (
          parameterSetName, gNa, gKv, stim, neuronName)

commands = [commandForNaKvStim(eachNa, eachKv, eachStim, eachNeuronName)
               for eachNeuronName in neuronNames
               for eachStim in stims
               for eachKv in xrange(gKvLow, gKvHigh + 1, stepSize)
               for eachNa in xrange(gNaLow, gNaHigh + 1, stepSize)]

for eachCommand in commands:
  print eachCommand
