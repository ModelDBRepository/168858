#!/usr/bin/python

import os

kExecutablePath = '/usr/local/nrn/x86_64/bin/nrngui'
kModelFilesDirectory = 'ModelFiles'
kHocFilesDirectory = 'HocFiles'
kDirectoryFile = 'ModelDirectory.csv'
kRelativeHocScriptsPath = 'Scripts/Hoc'
kParameterSetsFile = 'Scripts/ParameterSets.csv'

class PathsClass:

  def __init__(self):
    self._simulationProjectDir = os.getenv('SIMULATION_PROJECT', os.getcwd())

  def executablePath(self):
    return kExecutablePath

  def simulationProjectDir(self):
    return self._simulationProjectDir

  def directoryFile(self):
    return (self._simulationProjectDir + '/' + kModelFilesDirectory + '/' +
        kDirectoryFile)

  def parameterSetsFile(self):
    return self._simulationProjectDir + '/' + kParameterSetsFile

  def hocScriptsPath(self):
    """Returns the path to the directory containing NEURON scripts.
    By convention, Hoc scripts that serve solely to define a neuron are called
    'hoc files', whereas those that compute something or run a simulation are
    called 'hoc scripts'."""
    return self._simulationProjectDir + '/' + kRelativeHocScriptsPath

  def modelFilesPath(self):
    return self._simulationProjectDir + '/' + kModelFilesDirectory

  def hocFilesPath(self):
    """Returns the path to neuron-defining hoc files.
    By convention, Hoc scripts that serve solely to define a neuron are called
    'hoc files', whereas those that compute something or run a simulation are
    called 'hoc scripts'."""
    return self._simulationProjectDir + '/' + kHocFilesDirectory

  def toString(self):
    return """\
PathsClass:
  executablePath: %s
  simulationProjectDir: %s
  directoryFile: %s
  hocScriptsPath: %s
  modelFilesPath: %s
""" % (self.executablePath(), self.simulationProjectDir(), self.directoryFile(),
       self.hocFilePath(), self.modelFilesPath())

Paths = PathsClass()
