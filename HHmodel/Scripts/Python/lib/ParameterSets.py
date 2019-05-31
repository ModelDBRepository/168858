#!/usr/bin/python

from lib.Paths import *
from ParameterSet import ParameterSet

import sys

class ParameterSets:
  def __init__(self):
    self._path = Paths.parameterSetsFile()
    self._parameterSetsByName = {}

  def Load(self):
    filePointer = open(self._path, 'r')
    fileContents = filePointer.readlines()
    for eachLine in fileContents:
      parameters = ParameterSet()
      parameters.populateFromCsvRow(eachLine)
      self._parameterSetsByName[parameters.name()] = parameters

  def parameterSetForName(self, name):
    if not name in self._parameterSetsByName:
      print "Parameter set %s was requested, but not defined." % name
      sys.exit(1)
    parameterSet = self._parameterSetsByName[name]
    return parameterSet

