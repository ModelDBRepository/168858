#!/usr/bin/python

import copy
import math

class SwcNode:
  """Encapsulates a single Swc node"""

  def __init__(self, formatted_node):
    """Initializes a point from a test string.
    formatted_node: An swc-formatted text string describing a single node.
                    That is, a single line of an SWC text file.
    """
    text_elements = formatted_node.split()
    if len(text_elements) != 7:
      print "ERROR: Node formatted incorrectly."
    self._id = int(text_elements[0])
    self._type = int(text_elements[1])
    self._x = float(text_elements[2])
    self._y = float(text_elements[3])
    self._z = float(text_elements[4])
    self._radius = float(text_elements[5])
    self._parent_id = float(text_elements[6])
    self._children = []
    self._node_count_from_soma = -1

  def Id(self):
    return self._id

  # TODO(pcoskren): Have this return a constant so that client code doesn't have
  # to depend on a bare integer.
  def Type(self):
    """Returns the node's type:
       0: undefined
       1: soma
       2: axon
       3: basal
       4: apical
       5: branch point
       6: tip
       7: custom
    """
    return self._type

  def SetType(self, type):
    self._type = type

  def X(self):
    return self._x

  def Y(self):
    return self._y

  def Z(self):
    return self._z

  def Radius(self):
    return self._radius

  def ParentId(self):
    return self._parent_id

  def AddChild(self, node):
    self._children.append(node.Id())

  def Children(self):
    return self._children

  def SetNodeCountFromSoma(self, node_count):
    self._node_count_from_soma = node_count

  def NodeCountFromSoma(self):
    return self._node_count_from_soma

  def ToString(self):
    children_string = '[ '
    first = 1
    for each_id in self._children:
      if not first:
        children_string += ', '
      children_string += str(each_id)
      first = 0
    children_string += ' ]'
    return "%d\t%d\t%f\t%f\t%f\t%f\t%d\t%s" % (self._id, self._type, self._x,
                                               self._y, self._z, self._radius,
                                               self._parent_id, children_string)


