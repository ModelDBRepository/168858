#!/usr/bin/python

from lib import Neuron
from lib import NEURONInterface
from lib.Paths import *
from lib import Swc
from lib import SpineFile

import os
import re

class NeuronFileList:
  """Encapsulates the different model files for a single neuron."""

  def __init__(self, neuron_line):
    path_elements = neuron_line.strip().split('\t')
    if len(path_elements) != 9:
      print ":%s" % path_elements
      print "Error: neuron directory formatted incorrectly"
      print "Actual elements count: %d" % len(path_elements)
    self._name = path_elements[0].strip()
    arbor_string = path_elements[1].strip()
    self._age = path_elements[2].strip()
    self._microns_per_pixel_x = float(path_elements[3].strip())
    self._microns_per_pixel_y = float(path_elements[4].strip())
    self._microns_per_pixel_z = float(path_elements[5].strip())
    self._swc = Paths.modelFilesPath() + "/" + path_elements[6].strip()
    self._spines = Paths.modelFilesPath() + "/" + path_elements[7].strip()
    self._resting_potential = float(path_elements[8].strip())

    self.kCompleteArbor = 1
    self.kApicalArbor = 2
    self.kBasalArbor = 3
    self.kUnknownArbor = 4

    if arbor_string == 'complete':
      self._arbor = self.kCompleteArbor
    elif arbor_string == 'apical':
      self._arbor = self.kApicalArbor
    elif arbor_string == 'basal':
      self._arbor = self.kBasalArbor
    else:
      self._arbor = self.kUnknownArbor

  def Name(self):
    return self._name

  def Age(self):
    return self._age

  def Arbor(self):
    return self._arbor

  def MicronsPerPixelX(self):
    return self._microns_per_pixel_x

  def MicronsPerPixelY(self):
    return self._microns_per_pixel_y

  def MicronsPerPixelZ(self):
    return self._microns_per_pixel_z

  def ArborString(self):
    if self._arbor is self.kCompleteArbor:
      return 'complete'
    elif self._arbor is self.kApicalArbor:
      return 'apical'
    elif self._arbor is self.kBasalArbor:
      return 'basal'
    else:
      return 'unknown'

  def RestingPotential(self):
    return self._resting_potential

  def Swc(self):
    return self._swc

  def HasSwc(self):
    return self._swc != ''

  def HasReadableSwc(self):
    return self._swc != '' and self._swc != '-'

  def Spines(self):
    return self._spines

  def HasSpines(self):
    return self._spines != ''

  def HasReadableSpines(self):
    return self._spines != '' and self._spines != '-'

  def DebugString(self):
    return self.__dict__

class NeuronDirectory:
  """Encapsulates a list of the SWC and spine files of neurons.
  The list is assumed to be stored a tab-delimited file where each line
  begins with a '#' character (signifying the line is a comment), or
  contains the following fields:
    complete SWC file
    apical SWC file
    basal SWC file
    complete spine file
    apical spine file
    basal spine file
  """

  def __init__(self, parameterSet):
    self._path = Paths.directoryFile()
    self._neuron_lines = []
    self._neurons = []
    self._neurons_by_name = {}
    self._young_apical_neurons = []
    self._young_basal_neurons = []
    self._old_apical_neurons = []
    self._old_basal_neurons = []
    self._partial_neurons = []
    self._whole_neurons = []
    self._hoc_root = Paths.hocScriptsPath()
    self._swc_root = Paths.modelFilesPath()
    self._parameterSet = parameterSet

  def Load(self):
    file_pointer = open(self._path, 'r')
    file_contents = file_pointer.readlines()

    for each_line in file_contents[1:]:
      if each_line[0].strip() == '#': continue
      if each_line.strip() == '': continue
      each_neuron_line = NeuronFileList(each_line)
      each_line = each_line.strip()
      self._neuron_lines.append(each_neuron_line)
      each_neuron = Neuron.Neuron(
          each_neuron_line.Name(), each_neuron_line.Age(),
          each_neuron_line.ArborString(), each_neuron_line.MicronsPerPixelX(),
          each_neuron_line.MicronsPerPixelY(),
          each_neuron_line.MicronsPerPixelZ(), each_neuron_line.Swc(),
          each_neuron_line.Spines(), each_neuron_line.RestingPotential())
      each_neuron.SetHocRoot(self._hoc_root)
      each_neuron.SetStandardSomaRadius(self._parameterSet.stdSomaRadius())
      self._neurons.append(each_neuron)
      self._neurons_by_name[each_neuron.Name()] = each_neuron
      if each_neuron.Arbor() == each_neuron.kApicalArbor:
        self._partial_neurons.append(each_neuron)
        if each_neuron.Age() == 'young':
          self._young_apical_neurons.append(each_neuron)
        elif each_neuron.Age() == 'old':
          self._old_apical_neurons.append(each_neuron)
      elif each_neuron.Arbor() == each_neuron.kBasalArbor:
        self._partial_neurons.append(each_neuron)
        if each_neuron.Age() == 'young':
          self._young_basal_neurons.append(each_neuron)
        elif each_neuron.Age() == 'old':
          self._old_basal_neurons.append(each_neuron)
      elif each_neuron.Arbor() == each_neuron.kCompleteArbor:
        self._whole_neurons.append(each_neuron)

  def LoadNeurons(self):
    total_count = len(self._neurons)
    print 'Number of neurons in LoadNeurons: %d' % total_count
    file_count = 0
    for each_neuron in self._neurons:
      print "Loading neuron %s" % each_neuron.Name()
      each_neuron.Load()
      file_count += 1
      print "   ... done loading %d/%d" % (file_count, total_count)

  def LoadNeuronWithName(self, name):
    neuron = self.NeuronWithName(name)
    neuron.Load()

  def Names(self):
    """Return names of all neurons managed by the directory file, in a list."""

    names = []
    for each_neuron in self._neurons:
      names.append(each_neuron.Name())
    return names

  def Neurons(self):
    return self._neurons

  def NeuronWithName(self, name):
    return self._neurons_by_name[name]

  def YoungApicalNeurons(self):
    return self._young_apical_neurons

  def OldApicalNeurons(self):
    return self._old_apical_neurons

  def YoungBasalNeurons(self):
    return self._young_basal_neurons

  def OldBasalNeurons(self):
    return self._old_basal_neurons

  def PartialNeurons(self):
    return self._partial_neurons

  def WholeNeurons(self):
    return self._whole_neurons

  def ValidateFilesAreReadable(self):
    good_neuron_count = 0
    for each_neuron_line in self._neuron_lines:
      print "Checking %s" % each_neuron_line.Name()
      neuron_is_valid = 1

      if each_neuron_line.kUnknownArbor == each_neuron_line.Arbor():
        print "Arbor is unknown type."
        neuron_is_valid = 0

      if each_neuron_line.HasReadableSwc():
        swc = LuebkePaper.Swc.Swc(each_neuron_line.Swc())
        swc.Load()
        if not swc.Validate():
          print "Tree is NOT valid: %s" % swc.CurrentError()
          neuron_is_valid = 0

      if each_neuron_line.HasReadableSpines():
        spinefile = LuebkePaper.SpineFile.SpineFile(each_neuron_line.Spines())
        spinefile.Load()
      elif not each_neuron_line.HasSpines():
        print "Spines are missing"
        neuron_is_valid = 0

      if neuron_is_valid:
        good_neuron_count += 1
    print "%d/%d neurons are present and pass validation." % (
        good_neuron_count, len(self._neuron_lines))

  def ValidateSpinesMatchNodes(self):
    good_neuron_count = 0
    for each_neuron in self._neurons:
      neuron_is_valid = 1
      print ""
      print "========================"
      print "Checking %s" % each_neuron.Name()
      if each_neuron.HasSwcPath() and each_neuron.HasSpinesPath():
        if each_neuron.SpinesMatchNodes():
          print "  Complete: PASS"
        else:
          print "  Complete: FAIL"
          if not each_neuron.Arbor() == each_neuron.kCompleteArbor:
            neuron_is_valid = 0
          self._error = "Warning: Complete-neuron spines don't match nodes"
      else:
        print "Missing data for complete neuron"

      if neuron_is_valid:
        good_neuron_count += 1
        print "Neuron is valid."
      else:
        print "Neuron is NOT valid."

    print ""
    print "%d/%d neurons/spine sets are present and pass validation." % (
        good_neuron_count, len(self._neurons))

  def Validate(self):
    self.ValidateFilesAreReadable()
    self.ValidateSpinesMatchNodes()

  def ExpandNeuronNames(self, names):
    """Scans a list of names, replacing those that refer to groups of neurons with the actual names
       of the neurons in the group."""
    resultNeurons = []
    for eachName in names:
      if eachName == 'old-apical':
        resultNeurons.extend(self.OldApicalNeurons())
      elif eachName == 'old-basal':
        resultNeurons.extend(self.OldBasalNeurons())
      elif eachName == 'young-apical':
        resultNeurons.extend(self.YoungApicalNeurons())
      elif eachName == 'young-basal':
        resultNeurons.extend(self.YoungBasalNeurons())
      elif eachName == 'partial':
        resultNeurons.extend(self.PartialNeurons())
      elif eachName == 'whole':
        resultNeurons.extend(self.WholeNeurons())
      else:
        resultNeurons.append(self.NeuronWithName(eachName))
    return [eachNeuron.Name() for eachNeuron in resultNeurons]

