#!/usr/bin/python

from lib import NeuronDirectory
from lib import ParameterSets
from optparse import OptionParser

import itertools

# This should be called with /-delimited sequences of action-neuron pairs.  Each action-
# neuron pair is a comma-delimited list of actions, then a colon, then a comma-delimited list of
# neurons.  Optionally, this may be followed by another colon and a command-line option to be passed
# to the underlying command (any "--" prefix should be omitted).  Neurons can be specified by any
# name (or group name) recognized by the 'list.py' script.
#
# Examples:
# Scripts/Python/generateComputationCommands attenuation,geometry:old-apical,old-basal / mbpap:whole
# Scripts/Python/generateComputationCommands attenuation:old-apical,old-basal:nospines / mbpap:whole
#
# This approach lets you specify many commands at once, even if they are applied to different
# subsets of neurons.

parser = OptionParser()
parser.add_option("--params", action="store", type="string",
                  default="Christina-standard-testing",
                  help=("Name of the set of parameters that will be used in " +
                        "NEURON simulations supporting this computation, as " +
                        "specified in Scripts/ParameterSets.csv"))

def makeCommand(script, neuron, optionString):
  if len(optionString) > 0:
    return "Scripts/Python/%s %s %s;" % (script, neuron, optionString)
  else:
    return "Scripts/Python/%s %s;" % (script, neuron)

def printString(s): print s

def CommandsForCommandGroup(commandGroup, directory):
  """A commandgroup is a 2 or 3 item list.  The first is a comma-delimited list of actions, the
     second is a comma-delimited list of neuron names, and the third, if present, is the name of
     an option that should be passed to the commands."""
  actionString = commandGroup[0]
  neuronNameString = commandGroup[1]
  if len(commandGroup) > 2:
    optionString = "--" + commandGroup[2]
  else:
    optionString = ""

  actions = actionString.split(",")
  neuronNames = neuronNameString.split(",")
  neuronNames = directory.ExpandNeuronNames(neuronNames)

  return [makeCommand(a, n, optionString) for a in actions for n in neuronNames]

(options, args) = parser.parse_args()
parameterSetName = options.params
specificationString = "".join(args)

parameterSets = ParameterSets.ParameterSets()
parameterSets.Load()
parameterSet = parameterSets.parameterSetForName(parameterSetName)
directory = NeuronDirectory.NeuronDirectory(parameterSet)
directory.Load()

commandGroups = specificationString.split("/")
parsedCommandGroups = [CommandsForCommandGroup(x, directory) for x in
    [eachCommandGroup.split(":") for eachCommandGroup in commandGroups]]
commands = [command for eachList in parsedCommandGroups for command in eachList]

[printString(s) for s in commands]

