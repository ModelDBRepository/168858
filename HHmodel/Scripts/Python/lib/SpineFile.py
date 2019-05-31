#!/usr/bin/python

import lib.Swc

#   A tricky point that must be remembered: in NeuronStudio's output, spines
# are 0-indexed, nodes are 1-indexed.

class Spine:
  """Encapsulates a single spine."""

  def __init__(self, formatted_spine, path, line_number):
    """Initializes a spine from a test string.
    formatted_spine: A NeuronStudio spinefile-formatted text string describing
                     a single node. That is, a single line of a NeuronStudio
                     spine file.
    path: the path of the file from which the formatted spine was read
    line_number: the line number of the file at which the formatted spine
                     was read"""
    # 19 fields
    text_elements = formatted_spine.split()
    if len(text_elements) != 19:
      print "Error at %s:%d. spine formatted incorrectly" % (path,
                                                             line_number)
      for eachElement in text_elements:
        print eachElement
    try:
      self._id = int(text_elements[0])
      if text_elements[1] == 'N/A':
        self._section_number = -1
      else:
        self._section_number = int(text_elements[1])
      self._section_length = float(text_elements[2])
      if text_elements[3] == 'N/A':
        self._branch_order = -1
      else:
        self._branch_order = int(test_elements[3])
      self._x = float(text_elements[4])
      self._y = float(text_elements[5])
      self._z = float(text_elements[6])
      self._head_diameter = float(text_elements[7])
      if text_elements[8] == 'N/A':
        self._neck_diameter = -1
      else:
        self._neck_diameter = float(text_elements[8])
      if text_elements[9] == 'N/A':
        self._max_dts = -1
      else:
        self._max_dts = float(text_elements[9])
      self._type = text_elements[10]
      if text_elements[11] == 'yes':
        self._auto = 1
      else:
        self._auto = 0
      self._xyplane_angle = float(text_elements[12])
      self._swc_node_id = int(text_elements[13])
      self._swc_node_offset = float(text_elements[14])
      self._attach_x = float(text_elements[15])
      self._attach_y = float(text_elements[16])
      self._attach_z = float(text_elements[17])
      self._soma_distance = float(text_elements[18])
    except ValueError, instance:
      print "Error at %s:%d.  spine contains unparseable text.  %s" % (
          path, line_number, instance)

  def Id(self):
    return self._id

  def OffSetId(self, offset):
    self._id -= offset

  def SectionNumber(self):
    return self._section_number

  def SectionLength(self):
    return self._section_length

  def BranchOrder(self):
    return self._branch_order

  def X(self):
    return self._x

  def Y(self):
    return self._y

  def Z(self):
    return self._z

  def HeadDiameter(self):
    return self._head_diameter

  def NeckDiameter(self):
    return self._neck_diameter

  def MaxDTS(self):
    return self._max_dts

  def Type(self):
    return self._type

  def IsAuto(self):
    return self._auto

  def XYPlaneAngle(self):
    return self._xyplane_angle

  def SwcNodeId(self):
    return self._swc_node_id

  def SwcNodeOffset(self):
    return self._swc_node_offset

  def AttachX(self):
    return self._attach_x

  def AttachY(self):
    return self._attach_y

  def AttachZ(self):
    return self._attach_z

  def SomaDistance(self):
    return self._soma_distance

class SpineFile:
  """Encapsulate a NeuronStudio spine file.

  Note that the IDs in a spine file are not necessarily contiguous, because
  certain spines may be removed during loading, because they are attached to
  the soma or contain error values."""

  def __init__(self, path):
    """Initializes NeuronStudio spine file with path"""

    # CONSTANTS
    self._kSpineFreeNodesFromSoma = 3

    self._path = path
    self._spines = []
    self._spines_by_id = {}
    self._error = ''

  def Load(self, swc):
    file_pointer = open(self._path, 'r')
    file_contents = file_pointer.readlines()
    first_line = 1
    line_number = 1
    for each_line in file_contents:
      # The first line is just the column headers
      if first_line:
        first_line = 0
        continue
      each_spine = Spine(each_line, self._path, line_number)
      line_number = line_number + 1
      source_node_id = each_spine.SwcNodeId()
      # Address a possible bug where the spine node number can be one greater
      # than the end of the neuron.  (I'll consult Alfredo about this.)
      if source_node_id == swc.MaximumNodeNumber() + 1:
        source_node_id = swc.MaximumNodeNumber()
      if source_node_id == -1:
        continue  # NeuronStudio labels error spines as -1.  Ignore those.
      source_node = swc.NodeWithId(source_node_id)
      if not source_node:
        print "Warning %s:%d. spine references nonexistent node %s." % (
            self._path, line_number, source_node_id)
      elif source_node.NodeCountFromSoma() > self._kSpineFreeNodesFromSoma:
        self._spines.append(each_spine)
        self._spines_by_id[each_spine.Id()] = each_spine

  def Spines(self):
    return self._spines

  def SpineCount(self):
    return len(self._spines)

  def SpineAtIndex(self, index):
    return self._spines[index]

  def SpineWithId(self, id):
    return self._spines_by_id[id]

if __name__ == "__main__":
  spinefile = SpineFile('/Neurons/LocalRepositorySubset/ModelFiles/'
                        'Aug3_2006CellE/Aug3_2006CellE-apical-spines.txt')
  spinefile.Load()
  print "%d spines" % len(spinefile._spines)
