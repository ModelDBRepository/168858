#!/usr/bin/python

from lib import calcMeanBAP
from lib.Paths import Paths

import datetime
import subprocess
import os
import random
import re
import string
import sys

class AttenuationResults:
  def __init__(self):
    self.surface_area = -1
    self.spine_volume = -1
    self.spine_surface_area = -1
    self.outward_attenuations_by_frequency = {}
    self.inward_attenuations_by_frequency = {}

class NEURONInterface:
  def __init__(self, hocfile_path, parameterSet):
    self._hocfile_path = hocfile_path
    self._parameterSet = parameterSet

    # public.  These must match the values in readcell.hoc, when it checks the value of spine_type.
    self.kApicalSpines = 1
    self.kBasalSpines = 2
    self.kSubtreeSpecificSpines = 3

  def GetReadcellCommandString(self):
    readCellPath = Paths.hocScriptsPath() + "/readcell.hoc"
    with open(readCellPath) as readCellFile:
      readCellContents = readCellFile.read()
    return string.Template(readCellContents).substitute(self._parameterSet.dict())

  def GetEphysPropertiesCommandString(self, hocFilePath):
    path = Paths.hocScriptsPath() + "/ephys_properties.hoc"
    with open(path) as ephysPropertiesFile:
      ephysPropertiesContents = ephysPropertiesFile.read()
    substitutions = self._parameterSet.dict()
    substitutions["neuronPath"] = hocFilePath
    result = string.Template(ephysPropertiesContents).substitute(
        substitutions)
    return result

  def GetLoadScriptsCommandString(self, has_spines):
    if has_spines:
      flagSpinesValue = 1
    else:
      flagSpinesValue = 2

    loadScriptsString = """\
objref soma_ref
objref tree_root

load_file("fixnseg.hoc")
%s
load_file("actionPotentialPlayer.hoc")
load_file("analyticFunctions.hoc")
load_file("measureMeanAtten.hoc")

flag_spines = %d  // 1 = compensate for spines.  2 == don't compensate for spines
""" % (self.GetReadcellCommandString(), flagSpinesValue)
    return loadScriptsString

  def GetAttenuationsForNeuron(self, neuron, spine_type, has_spines):
    commandString = ('E_PAS=%f\n'
                     'STD_SOMA=%s\n'
                     '%s\n'
                     'readcell("%s", %d)\n'
                     'soma {\n nseg = 1\n soma_ref = new SectionRef()\n}\n'
                     'dend_whole[0] {\n tree_root = new SectionRef()\n}\n'
                     'meanInwardAttenuationAllFrequencies(soma_ref, tree_root)\n'
                     'meanOutwardAttenuationAllFrequencies(soma_ref, tree_root)\n'
                     'print "done"\n'
                     'quit()\n') % (neuron.RestingPotential(),
                                    neuron.StandardSomaRadius(),
                                    self.GetLoadScriptsCommandString(has_spines),
                                    neuron.HocFilePath(), spine_type)
    response_lines = self._runCommandsInNeuron(commandString)
    if (response_lines == ""):
      return

    surface_area_searcher = re.compile("surface area: ([\d.]+)")
    spine_volume_searcher = re.compile("spine volume: ([\d.]+)")
    spine_surface_area_searcher = re.compile("spine surface area: ([\d.]+)")
    outward_attenuation_searcher = re.compile(
        "Frequency: ([\d.]+) Outward mean attenuation: ([\d.]+)")
    inward_attenuation_searcher = re.compile(
        "Frequency: ([\d.]+) Inward mean attenuation: ([\d.]+)")

    results = AttenuationResults()

    match = None
    for each_line in response_lines:
      match = outward_attenuation_searcher.search(each_line)
      if match:
        frequency = int(match.group(1))
        attenuation = float(match.group(2))
        results.outward_attenuations_by_frequency[frequency] = attenuation
        continue
      match = inward_attenuation_searcher.search(each_line)
      if match:
        frequency = int(match.group(1))
        attenuation = float(match.group(2))
        results.inward_attenuations_by_frequency[frequency] = attenuation
        continue
      match = spine_surface_area_searcher.search(each_line)
      if match:
        results.spine_surface_area = float(match.group(1))
        continue
      match = spine_volume_searcher.search(each_line)
      if match:
        results.spine_volume = float(match.group(1))
        continue
      match = surface_area_searcher.search(each_line)
      if match:
        results.surface_area = float(match.group(1))
        continue
    return results


  def GetBPAPForNeuron(self, neuron, spine_type, has_spines):
    """Retrieve mean backpropagating action potential data for neuron.
       Returns a list of tuples (arclength from soma, maximum displacement from
       rest potential."""
    command_string = ('E_PAS=%f\n'
                      '%s\n'
                      'STD_SOMA=%s\n'
                      'readcell("%s", %d)\n'
                      'soma {\n nseg = 1\n soma_ref = new SectionRef()\n}\n'
                      'print "--BEGIN BPAP--"\n'
                      'BAPvalues(soma_ref, voltage_vec, time_vec, "dend")\n'
                      'print "--END BPAP--"\n'
                      'quit()\n' % (neuron.RestingPotential(),
                                    self.GetLoadScriptsCommandString(has_spines),
                                    neuron.StandardSomaRadius(),
                                    neuron.HocFilePath(), spine_type))
    raw_response_lines = self._runCommandsInNeuron(command_string)

    result = []
    in_data = False
    for each_line in raw_response_lines:
      if not (-1 == each_line.find('--BEGIN BPAP--')):
        in_data = True
        continue
      if each_line == '--END BPAP--':
        in_data = False
        continue
      if in_data:
        points_as_strings = each_line.split()
        result.append((float(points_as_strings[0]),
                       float(points_as_strings[1])))
    return result


  def GetRnForNeuron(self, neuron):
    command_string = ("""\
E_PAS=%f
STD_SOMA=%s
load_file("fixnseg.hoc")
%s
%s
printInputResistanceValuesForNeuron(neuron_path)
quit()
""" % (neuron.RestingPotential(), neuron.StandardSomaRadius(),
       self.GetReadcellCommandString(),
       self.GetEphysPropertiesCommandString(
          neuron.HocFilePath(distinguish_apical_basal=True))))

    responseLines = self._runCommandsInNeuron(command_string)

    firingRateByInputCurrentMatcher = re.compile(r"(-?\d\.0[0-5])\s+(-?[\d.]+)")
    firingRates = []
    for eachLine in responseLines:
      match = firingRateByInputCurrentMatcher.search(eachLine)
      if match:
        current = float(match.group(1))
        firingRate = float(match.group(2))
        firingRates.append(current)
        firingRates.append(firingRate)
    inputResistance = self._extractSlopeFromPoints(firingRates)
    return inputResistance


  def GetFiringRateForNeuron(self, neuron, totalAppliedCurrent, gNa, gKv):
    if not (gNa is None) and not (gKv is None):
      self._parameterSet.setGNa(gNa)
      self._parameterSet.setKv(gKv)

    # The firing rate simulations can use a different value of nseg than the
    # morphological simulations.  However, they load neurons the same way, and
    # that procedure, in readcell.hoc, is where the nseg values are set.  Rather
    # than refactor that whole process, this code just substitutes the value
    # into the location where readcell.hoc expects it to be.
    self._parameterSet.setGeomNsegDlambda(
        self._parameterSet.geomNsegDlambdaForFiringRates())

    commandString = ("""\
E_PAS=%s
STD_SOMA=%s
load_file("fixnseg.hoc")
%s
%s
simulateCurrentStep_withIHold(100, 1100, %f, 1, "tmp")
quit()
""" % (self._parameterSet.ePas(), neuron.StandardSomaRadius(),
       self.GetReadcellCommandString(),
       self.GetEphysPropertiesCommandString(
          neuron.HocFilePath(distinguish_apical_basal=True)),
       totalAppliedCurrent))

    responseLines = self._runCommandsInNeuron(commandString)
    firingRateMatcher = re.compile(r"Mean firing rate: ([\d.]+)")
    for eachLine in responseLines:
      match = firingRateMatcher.search(eachLine)
      if match:
        return float(match.group(1))

  def _extractSlopeFromPoints(self, firingRates):
    firingRateArgs = [str(x) for x in firingRates]
    popenObject = subprocess.Popen(
        ("/usr/bin/Rscript Scripts/R/slopeOfLine.r " +
            " ".join(firingRateArgs)),
        stdout=subprocess.PIPE, shell = 1)
    stdoutString = popenObject.communicate()
    popenObject.wait()
    return float(stdoutString[0].strip())

  def _runCommandsInNeuron(self, commandString):
    today = datetime.date.today()
    year = today.year
    month = today.month
    day = today.day

    logIdentifier = "-" + str(long(random.random() * 1000000))

    with open("Logs/firingRateCommand-%d-%02d-%02d%s.log" % (year, month, day,
                  logIdentifier), "a") as commandLog:
      commandLog.write("-------------------------------------------\n")
      commandLog.write(commandString)
    popenObject = subprocess.Popen(
        "cd %s; %s -nobanner -notatty" % (
            self._hocfile_path, Paths.executablePath()),
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=1)
    try:
      (stdoutString, stderrString) = popenObject.communicate(commandString)
      popenObject.wait()
    except KeyboardInterrupt:
      KillNeuronProcess(popenObject.pid)
      return ""
    with open("Logs/firingRate-%d-%02d-%02d%s.stdout" % (year, month, day,
        logIdentifier), "a") as simulationStdout:
      simulationStdout.write(stdoutString)
    if not stderrString is None:
      with open("Logs/firingRate-%d-%02d-%02d%s.stderr" % (year, month,
          day, logIdentifier), "a") as simulationStderr:
        simulationStderr.write(stderrString)

    return stdoutString.splitlines()

def _lineWithSubstitutedParameters(line, parameterSet):
  match = search(r"-!-(.*?)-!-", line)
  if match == None:
    return line
  parameterName = match.group(1)
  value = parameterSet.valueForKey(parameterName)

def _getTemplatedHocFile(self, filename):
  """Returns the text of the hoc file with parameters substituted."""
  fullPath = "%s/%s" % (self._hocfile_path, filename)
  with open(fullPath) as file:
    result = "\n".join(
        [_lineWithSubstitutedParameters(eachLine.strip(), self._parameterSet)
            for eachLine in file])
  print "-------------- begin hocfile"
  print result
  print "-------------- end hocFile"
  return result

def KillNeuronProcess(pidToKill):
  """Kill the subordinate NEURON process.
  The trick here is that the process we open is a shell script, which opens
  a shell script, which opens nrniv.  Killing the script doesn't kill the
  subordinate process."""
  nrnivPsLines = [x.rstrip('\n').split()
      for x in os.popen("ps j | grep nrniv | grep -v grep")]
  nrnivPids = [x[1] for x in nrnivPsLines]
  for eachPid in nrnivPids:
    ancestors = AncestorsPidsForPid(eachPid)
    if str(pidToKill) in ancestors:
      neuronPid = ancestors[0]
      os.kill(int(neuronPid), 9)

def AncestorsPidsForPid(pid):
  """Returns a list containing the chain of parent pids above the specified pid."""
  ancestry = [pid]
  parent = parentForPid(pid)
  while (parent):
    ancestry.append(parent)
    parent = parentForPid(parent)
  return ancestry

def parentForPid(pid):
  parentPidLines = [x.rstrip('\n').split()
      for x in os.popen("ps -j -p %s | grep %s" % (pid, pid))]
  if len(parentPidLines) == 0:
    return None
  parentPid = parentPidLines[0][2]
  return parentPid



