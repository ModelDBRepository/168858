#!/usr/bin/python

import lib.Swc
import lib.SpineFile
import math
import decimal

#   A tricky point that must be remembered: in NeuronStudio's output, spines
# are 0-indexed, nodes are 1-indexed.

class Section:
  """Represents an unbranched length of dendrite.

    Position and radius both vary along the length of the section.  A neuron's
    soma is not considered a part of any section, but unparented sections abut
    it."""

  def __init__(self, id, parent_id):
    self._id = id
    self._nodes = []
    self._children = []  # List of Sections
    self._children_section_ids = []  # List of ints.
    self._parent_id = parent_id  # -1 means soma
    self._length = 0  # microns
    self._start_length_to_soma = 0

  def Id(self):
    return self._id

  def Nodes(self):
    return self._nodes

  def GetCopy(self):
    """Returns a new Section object, with its own lists of nodes and children.
       However, the actual members of those lists will not be copied, and all
       other values will be identical."""
    result_copy = Section(self._id, self._parent_id)
    result_copy._nodes = list(self._nodes)
    result_copy._children = list(self._children)
    result_copy._children_section_ids = list(self._children_section_ids)
    result_copy._parent_id = self._parent_id
    result_copy._length = self._length
    result_copy._start_length_to_soma = self._start_length_to_soma
    return result_copy

  def SetNodes(self, nodes):
    self._nodes = nodes

  def Children(self):
    return self._children

  def ChildrenSectionIds(self):
    return self._children_section_ids

  def ParentId(self):
    return self._parent_id

  def SetParentId(self, parent_id):
    self._parent_id = parent_id

  def AddNode(self, swc_node):
    if len(self._nodes) > 0:
      previous_node = self._nodes[-1]
      distance = self._NodeDistance(previous_node, swc_node)
      self._length += distance
    self._nodes.append(swc_node)

  def AddChild(self, child_section):
    self._children.append(child_section)
    self._children_section_ids.append(child_section.Id())

  def ClearChildren(self):
    self._children = []

  def ClipStartingNodesLargerThanRadius(self, radius):
    pass

  def Length(self):
    return self._length

  # Surface area of a conical segment is 2 * pi * r * s, where s is arclength and
  # r is the mean of the radii at the beginning and end of the segment.  Note
  # that this differs from how NEURON computes surface area.
  def SurfaceAreaNodeToNode(self, node1, node2):
    length = self._NodeDistance(node1, node2)
    radius1 = node1.Radius()
    radius2 = node2.Radius()
    radius_average = (radius1 + radius2) / 2.0
    radius_diff = radius2 - radius1
    arclength = math.sqrt(length * length + radius_diff * radius_diff)
    return math.pi * 2.0 * radius_average * arclength

  # Surface area of a conical segment is 2 * pi * r * s, where s is arclength and
  # r is the mean of the radii at the beginning and end of the segment.  Note
  # that this differs from how NEURON computes surface area.
  def SurfaceArea(self):
    if len(self._nodes) < 2:
      return 0.0
    area = 0.0

    previous_node = self._nodes[0]
    for each_node in self._nodes[1:]:
      area += self.SurfaceAreaNodeToNode(previous_node, each_node)
      previous_node = each_node
    return area

  def Volume(self):
    if len(self._nodes) < 2:
      return 0.0
    volume = 0.0

    previous_node = self._nodes[0]
    for each_node in self._nodes[1:]:
      length = self._NodeDistance(previous_node, each_node)
      radius_prev = previous_node.Radius()
      radius_this = each_node.Radius()
      radius_diff = radius_this - radius_prev
      arclength = math.sqrt(length * length + radius_diff * radius_diff)
      volume += (1.0 / 3.0) * math.pi * length * (radius_prev * radius_prev +
          radius_prev * radius_this + radius_this * radius_this)
      previous_node = each_node
    return volume

  def DistanceIsInBand(self, distance, band_start, band_end):
    return distance >= band_start and distance < band_end

  def SectionLengthInBand(self, band_start, band_end):
    first_node_in_band = -1
    last_node_in_band = -1

    # To speed things up, precompute the distances of all nodes in this
    # section.  The node_distances vector is the same length of self._nodes,
    # and contains distances to the soma in a one-to-one relationship.
    node_distances = []
    for each_node in self._nodes:
      node_distances.append(self.LengthToNodeFromSoma(each_node))

    # Check whether we actually intersect the band.  This isn't strictly
    # necessary, since sections that don't intersect will just contribute 0
    # length below, but this lets us exit the function earlier and saves some
    # time.
    for i in range(0, len(self._nodes)):
      each_node = self._nodes[i]
      length_to_node = node_distances[i]
      if length_to_node >= band_start and length_to_node < band_end:
        first_node_in_band = i
        break
    for i in reversed(xrange(0, len(self._nodes))):
      each_node = self._nodes[i]
      length_to_node = node_distances[i]
      if self.DistanceIsInBand(node_distances[i], band_start, band_end):
        last_node_in_band = i
        break
    if first_node_in_band == -1 or last_node_in_band == -1:
      return 0
    start_scan_index = None
    end_scan_index = None

    # If the section is entirely within the band, then scanning from the first
    # node to the last node is correct.  Otherwise, we need to scan from the
    # one before the first in-band to the one after the last in-band, in order
    # to catch the portion of the between-node line segment that lays within
    # the band.  Again, this isn't necessary, but should save some execution
    # time.
    if first_node_in_band > 0:
      start_scan_index = first_node_in_band - 1
    else:
      start_scan_index = first_node_in_band
    if last_node_in_band == len(self._nodes) - 1:
      end_scan_index = last_node_in_band
    else:
      end_scan_index = last_node_in_band + 1

    # Okay, this is the core of the function.
    section_length = 0
    for i in range(start_scan_index, end_scan_index):
      each_node = self._nodes[i]
      each_distance = node_distances[i]
      # Next_node will be end_scan_index on the last iteration
      next_node = self._nodes[i + 1]
      next_distance = node_distances[i + 1]
      if (self.DistanceIsInBand(each_distance, band_start, band_end) and
          self.DistanceIsInBand(next_distance, band_start, band_end)):
        section_length += (next_distance - each_distance)
      elif (not self.DistanceIsInBand(each_distance, band_start, band_end) and
            self.DistanceIsInBand(next_distance, band_start, band_end)):
        section_length += (next_distance - band_start)
      elif (self.DistanceIsInBand(each_distance, band_start, band_end) and
            not self.DistanceIsInBand(next_distance, band_start, band_end)):
        section_length += (band_end - each_distance)
      else:
        # Do nothing: this chunk of the section doesn't intersect the band.
        pass
    return section_length

  def SetLengthFromSomaToSection(self, length):
    self._start_length_to_soma = length

  def LengthToStartFromSoma(self):
    return self._start_length_to_soma

  def LengthToNodeFromSoma(self, swc_node):
    return self._start_length_to_soma + self.LengthToNode(swc_node)

  def LengthToPrevious(self, swc_node):
    """Returns the length from this node to the node preceding it.

       Returns 0 if swc_node is the first node of the segment."""
    previous_node = None
    for each_node in self._nodes:
      if swc_node is each_node:
        if previous_node:
          return self._NodeDistance(previous_node, each_node)
        else:
          return 0
      previous_node = each_node
    return 0  # Only here if the node isn't found.

  def LengthToNode(self, swc_node):
    """Returns the length from the start of the segment to the specified node.
    """
    length = 0
    previous_node = None
    for each_node in self._nodes:
      if not previous_node and swc_node is each_node:
        return length
      if not previous_node:
        previous_node = each_node
        continue
      length += self._NodeDistance(previous_node, each_node)
      if swc_node is each_node:
        return length
      previous_node = each_node
    return length

  def _NodeDistance(self, node1, node2):
    return math.sqrt(math.pow(node1.X() - node2.X(), 2) +
                              math.pow(node1.Y() - node2.Y(), 2) +
                              math.pow(node1.Z() - node2.Z(), 2))

  def PercentageLengthOfNode(self, swc_node):
    return self.LengthToNode(swc_node) / self.Length()

  def IntersectsRadius(self, radius, base_radius):
    """ Returns true if the section intersects the specified Sholl radius.
        radius is the Sholl radius relative to the soma.
        base_radius is the distance, along the dendrite, to the base of this
          section, so that the section knows where it's positioned in the global
          space of the neuron.
    """
    first_node = self._nodes[0]
    last_node = self._nodes[-1]
    first_node_distance = base_radius + self.LengthToNode(first_node)
    last_node_distance = base_radius + self.LengthToNode(last_node)
    return (first_node_distance <= radius and last_node_distance > radius)

  def DiameterOfIntersectionAtDistance(self, distance_along_section):
    if (len(self._nodes) < 2):
      return -1
    node = None
    next_node = None
    distance_to_node = None
    distance_to_next_node = None
    found_node = False
    for i in range(0, len(self._nodes) - 1):
      node = self._nodes[i]
      next_node = self._nodes[i + 1]
      distance_to_node = self.LengthToNode(node)
      distance_to_next_node = self.LengthToNode(next_node)
      if (distance_to_node <= distance_along_section and
          distance_to_next_node > distance_along_section):
        found_node = True
        break
    if not found_node:
      return -1
    diameter_of_node = node.Radius() * 2.0
    diameter_of_next_node = next_node.Radius() * 2.0
    diameter_at_radius = ( ( (distance_along_section - distance_to_node) /
                             (distance_to_next_node - distance_to_node) ) *
                           (diameter_of_next_node - diameter_of_node) +
                           diameter_of_node )
    return diameter_at_radius
