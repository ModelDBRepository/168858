#!/usr/bin/python

from lib.SwcNode import SwcNode

import copy
import math

class Swc:
  """Encapsulate an Swc file.
     The Swc class encapsulates a single Swc file, providing access to both
     read and write functions."""

  def __init__(self, path):
    """Initializes Swc object with path.
       Path can be absolute or relative to the script's invocation path.
       Nodes, proceeding from the root to the first branch point, are discarded
       until a node with less than maximumApicalRootDiameter is encountered.
       A value of -1 for maximumApicalDiameter signals that no nodes should be
       discarded.  Only apical nodes (as defined by SwcNode.Type() are ever
       discarded."""
    self._path = path
    self._nodes = []
    self._root_node = None
    self._error = ''
    self._error_details = {}
    self._tree = {}  # nodes by id.
    self._type_histo = { 0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0 }
    self._lines = {}  # Original lines in the SWC file
    self._max_node_number = -1

  def Load(self):
    file_pointer = open(self._path, 'r')
    file_contents = file_pointer.readlines()
    line_index = 0  # To report errors; 1-indexed
    for each_line in file_contents:
      line_index = line_index + 1
      self._lines[line_index] = each_line
      if each_line[0] == '#': continue
      if each_line.strip() == '': continue
      each_node = SwcNode(each_line)
      self._nodes.append(each_node)

      # Be sure the id is unique
      if each_node.Id() in self._tree:
        self._error = "Neuron contains multiple nodes with the same id."
        self._error_details['line'] = line_index;
        self._error_details['node id'] = each_node.Id()
        break;
      if each_node.Id() > self._max_node_number:
        self._max_node_number = each_node.Id()
      self._tree[each_node.Id()] = each_node
      type = each_node.Type()
      self._type_histo[type] = self._type_histo[type] + 1
      if each_node.ParentId() == -1:  # Root node, don't check for parent.
        self._root_node = each_node
        each_node.SetNodeCountFromSoma(0)
        continue
      if not self._tree.has_key(each_node.ParentId()):
        self._error = "Node %d refers to nonexistent parent %d." % (
            each_node.Id(), each_node.ParentId())
        self._error_details['line'] = line_index
        break;
      parent_node = self._tree[each_node.ParentId()]
      self._tree[each_node.ParentId()].AddChild(each_node)
      each_node.SetNodeCountFromSoma(parent_node.NodeCountFromSoma() + 1)

  def NodeWithId(self, id):
    if id in self._tree:
      return self._tree[id]
    else:
      return None

  def MaximumNodeNumber(self):
    return self._max_node_number

  def _NodeDistance(self, node1, node2):
    return math.sqrt(math.pow(node1.X() - node2.X(), 2) +
                              math.pow(node1.Y() - node2.Y(), 2) +
                              math.pow(node1.Z() - node2.Z(), 2))

  def RootNode(self):
    return self._root_node

  def ValidateHasNoError(self):
    return (self._error == '')

  def ValidateIsLoaded(self):
    if len(self._nodes) == 0:
      self._error = "Neuron has not been loaded."
    else:
      return 1

  def ValidateHasOneSoma(self):
    soma_count = self._type_histo[1];
    if 0 == soma_count:
      self._error = "Neuron does not have a soma."
      return 0
    elif soma_count > 1:
      self._error = "Neuron has multiple somas."
      self.PrintTypeHistogram()
      return 0
    else:
      return 1

  def ValidateHasOneRoot(self):
    roots = [each_node
        for each_node in self._nodes
        if each_node.ParentId() == -1]
    if 0 == len(roots):
      self._error = "Neuron does not have a root node."
      return 0
    elif len(roots) > 1:
      self._error = "Neuron has multiple root nodes."
      self.PrintTypeHistogram()
      return 0
    else:
      return 1

  def ValidateHasNoUnknowns(self):
    unknown_count = self._type_histo[0];
    if 0 != unknown_count:
      self._error = "Neuron contains nodes of unknown type."
      self.PrintTypeHistogram()
      return 0;
    else:
      return 1;

  def NumberTipsAndBranches(self):
    return self._type_histo[5] + self._type_histo[6]

  def PrintTree(self):
    for each_value in self._tree.values():
      print each_value.ToString()

  def ValidateIsConnected(self):
    # List of visited nodes; it's a hash to speed up deleting
    local_tree = {}
    for each_key in self._tree:
      local_tree[each_key] = 1

    # Find the soma, which is usually node 1, but not necessarily.
    for each_node in self._tree.values():
      if 1 == each_node.Type():
        soma = each_node
        break

    nodes_to_scan = []
    current_root = soma
    nodes_to_scan.extend(current_root.Children())
    del local_tree[current_root.Id()]

    scanning_node_id = nodes_to_scan.pop()
    while scanning_node_id:
      if not scanning_node_id in local_tree:
        continue
      scanning_node = self._tree[scanning_node_id]
      nodes_to_scan.extend(scanning_node.Children())
      del local_tree[scanning_node_id]
      if len(nodes_to_scan):
        scanning_node_id = nodes_to_scan.pop()
      else:
        scanning_node_id = None
    return (len(local_tree) == 0)

  def Validate(self):
    return (self.ValidateHasNoError() and self.ValidateIsLoaded() and
            self.ValidateHasOneSoma() and self.ValidateHasOneRoot() and
            self.ValidateHasNoUnknowns() and self.ValidateIsConnected())

  def CurrentError(self):
    """Returns the current error, then resets it."""
    result = self._error
    self._error = ''
    return result

  def PrintTypeHistogram(self):
    print "0: %d" % self._type_histo[0]
    print "1: %d" % self._type_histo[1]
    print "2: %d" % self._type_histo[2]
    print "3: %d" % self._type_histo[3]
    print "4: %d" % self._type_histo[4]
    print "5: %d" % self._type_histo[5]
    print "6: %d" % self._type_histo[6]
    print "7: %d" % self._type_histo[7]

  def BoundingBox(self):
    """Returns a tuple ((x, y, z), (x, y, z)) that bounds the SWC structure.
    """
    if len(self._nodes) < 2:
      return ((0, 0, 0), (0, 0, 0))
    start_node = self._nodes[0]
    min_x = start_node.X()
    min_y = start_node.Y()
    min_z = start_node.Z()
    max_x = start_node.X()
    max_y = start_node.Y()
    max_z = start_node.Z()
    for each_node in self._nodes[1:]:
      (x, y, z) = (each_node.X(), each_node.Y(), each_node.Z())
      if x < min_x:
        min_x = x
      if x > max_x:
        max_x = x
      if y < min_y:
        min_y = y
      if y > max_y:
        max_y = y
      if z < min_z:
        min_z = z
      if z > max_z:
        max_z = z
    return ((min_x, min_y, min_z), (max_x, max_y, max_z))


if __name__ == "__main__":
  swc_neuron = Swc('/Neurons/LocalRepositorySubset/ModelFiles/Aug3_2006CellE/'
                   'Aug3_2006CellE-total.swc')
  swc_neuron.Load()
  if swc_neuron.Validate():
    print "Neuron is valid"
  else:
    print "Neuron is NOT valid: %s" % swc_neuron.CurrentError()
  swc_neuron.ReplaceBranchAndTipNodesWithApicalBasal()
  swc_neuron.PrintTypeHistogram()
