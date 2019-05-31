#!/usr/bin/python

from lib.HocFile import HocFile
from lib.Section import *
from lib.Swc import Swc
from lib.SpineFile import SpineFile

import math
import decimal

#   A tricky point that must be remembered: in NeuronStudio's output, spines
# are 0-indexed, nodes are 1-indexed.

class Neuron:
  """Represents a complete neuron, with dendrites and spines."""

  def __init__(self, name, age, arbor_string, microns_per_pixel_x,
               microns_per_pixel_y, microns_per_pixel_z, swc_path, spines_path,
               resting_potential):
    self._name = name
    self._age = age
    self._microns_per_pixel_x = microns_per_pixel_x
    self._microns_per_pixel_y = microns_per_pixel_y
    self._microns_per_pixel_z = microns_per_pixel_z
    if swc_path == '-':
      self._swc_path = ''
    else:
      self._swc_path = swc_path
    self._hoc_path = ''
    self._hoc_root = ''
    if spines_path == '-':
      self._spines_path = ''
    else:
      self._spines_path = spines_path
    self._resting_potential = resting_potential
    self._swc = None
    # TODO(pcoskren): the following should really be named _spines_file, and its
    # accessor named SpinesFile, to avoid the confusing neuron.Spines().Spines()
    # pattern that shows up in a few places.
    self._spines = None
    self._sections = []
    self._apical_sections = []
    self._basal_sections = []
    self._sections_by_node = {}
    self._sections_by_id = {}
    self._is_loaded = False

    # The soma is technically the root of the entire tree, but it is not
    # considered a part of any of the sections.  Therefore, there can be (and
    # usually are, unless the SWC file consists solely of an apical tree)
    # multiple root sections
    self._root_sections = []

    self.kCompleteArbor = 1
    self.kApicalArbor = 2
    self.kBasalArbor = 3
    self.kUnknownArbor = 4

    # These values are taken from, and must match the values in, readcell.hoc.
    self.kApicalHeadDiam = .47
    self.kApicalHeadLen = .71
    self.kApicalNeckDiam = .19
    self.kApicalNeckLen = .44
    self.kBasalHeadDiam = .56
    self.kBasalHeadLen = .82
    self.kBasalNeckDiam = .16
    self.kBasalNeckLen = .54

    if arbor_string == 'complete':
      self._arbor = self.kCompleteArbor
    elif arbor_string == 'apical':
      self._arbor = self.kApicalArbor
    elif arbor_string == 'basal':
      self._arbor = self.kBasalArbor
    else:
      self._arbor = self.kUnknownArbor

    self._standard_soma_radius = -1;

  def Load(self):
    if (self._is_loaded):
      return
    self._swc = Swc(self._swc_path)
    self._swc.Load()
    root_node = self._swc.RootNode()
    if not root_node:
      print "Error %s.  No root node present" % self._swc_path
    child_node_ids = root_node.Children()
    next_id = 0
    for each_id in child_node_ids:
      each_child = self._swc.NodeWithId(each_id)
      section = Section(next_id, -1)
      self._sections.append(section)
      if (3 == each_child.Type()):  # basal
        self._basal_sections.append(section)
      if (4 == each_child.Type()):  # apical
        self._apical_sections.append(section)
      self._sections_by_id[next_id] = section
      self._root_sections.append(section)
      last_sub_id = self._SplitIntoSections(self._swc, each_child, section)
      next_id = last_sub_id + 1

    if (self.HasSpinesPath()):
      self._spines = SpineFile(self._spines_path)

      self._spines.Load(self._swc)
    else:
      print "Warning: no spines for neuron %s" % self.Name()
    self._is_loaded = True

  def _SplitIntoSections(self, swc, root_node, section):
    """ Returns the last id assigned to a section. """
    if not self._swc:
      return
    last_id = section.Id()
    section.AddNode(root_node)
    self._sections_by_node[root_node] = section
    child_node_ids = root_node.Children()
    last_child_node = root_node
    while len(child_node_ids) == 1:  # Only 1 child == straight line
      child_node = swc.NodeWithId(child_node_ids[0])
      if child_node == None:
        print "Ai!  Child node is None:"
        x = 0/0
      section.AddNode(child_node)
      self._sections_by_node[child_node] = section
      last_child_node = child_node
      child_node_ids = child_node.Children()
    if len(child_node_ids) > 1:
      next_id = last_id + 1
      for each_node_id in child_node_ids:
        child_node = swc.NodeWithId(each_node_id)
        new_section = Section(next_id, section.Id())
        section.AddChild(new_section)
        # Note that we don't add to self._sections_by_node here.  That would
        # lead to the same node appearing as a key more than once.  Since the
        # position of a spine is between a node and its parent, and
        # self._sections_by_node is intended for spine calculations, it makes
        # sense to make branch nodes index the section for which they are the
        # last node, rather than the first, so that the parent is on the same
        # section.
        self._sections.append(new_section)
        if (3 == child_node.Type()):  # basal
          self._basal_sections.append(new_section)
        if (4 == child_node.Type()):  # apical
          self._apical_sections.append(new_section)
        self._sections_by_id[next_id] = new_section
        new_section.AddNode(last_child_node)
        last_id = self._SplitIntoSections(swc, child_node, new_section)
        next_id = last_id + 1
    return last_id

  def Name(self):
    return self._name

  def Age(self):
    return self._age

  def Arbor(self):
    return self._arbor

  def ArborString(self):
    if self._arbor == self.kCompleteArbor:
      return 'complete'
    elif self._arbor == self.kApicalArbor:
      return 'apical'
    elif self._arbor == self.kBasalArbor:
      return 'basal'
    else:
      return 'unknown'

  def MicronsPerPixelX(self):
    return self._microns_per_pixel_x

  def MicronsPerPixelY(self):
    return self._microns_per_pixel_y

  def MicronsPerPixelZ(self):
    return self._microns_per_pixel_z

  def SwcPath(self):
    return self._swc_path

  def HasSwcPath(self):
    return (self._swc_patc != '')

  def SetHocRoot(self, path):
    self._hoc_root = path

  def HocRoot(self):
    return self._hoc_root

  def HocFilePath(self, distinguish_apical_basal=False):
    if distinguish_apical_basal:
      return "%s/%s-apicalbasal-spiny.hoc" % (self._hoc_root, self.Name())
    else:
      return "%s/%s-spiny.hoc" % (self._hoc_root, self.Name())

  def SpinesPath(self):
    return self._spines_path

  def HasSpinesPath(self):
    return (self._spines_path != '')

  def RestingPotential(self):
    return (self._resting_potential)

  def RootNode(self):
    return self._swc.RootNode()

  def NodeWithId(self, id):
    return self._swc.NodeWithId(id)

  def DendriteSectionCount(self):
    return len(self._sections)

  def ApicalSectionCount(self):
    return len(self._apical_sections)

  def BasalSectionCount(self):
    return len(self._basal_sections)

  def MeanSectionLength(self):
    total_length = 0
    section_count = 0
    for each_section in self._sections:
      total_length += each_section.Length()
      section_count += 1
    return total_length / section_count

  def SectionAtIndex(self, index):
    return self._sections[index]

  def SectionWithId(self, id):
    return self._sections_by_id[id]

  def SectionForNode(self, swc_node):
    if swc_node in self._sections_by_node:
      return self._sections_by_node[swc_node]
    else:
      print ("Error: section requested for swc_node id %d, which is not "
          "associated with a section") % swc_node.Id()
      return None

  def Sections(self):
    return self._sections

  def ApicalSections(self):
    return self._apical_sections

  def BasalSections(self):
    return self._basal_sections

  def RootSections(self):
    return self._root_sections

  def SpineCount(self):
    if not self._spines:
      return 0
    else:
      return self._spines.SpineCount()

  def CumulativeLength(self):
    total_length = 0
    for each_section in self.Sections():
      total_length += each_section.Length()
    return total_length

  def SurfaceArea(self):
    total_area = 0
    for each_section in self.Sections():
      total_area += each_section.SurfaceArea()
    if self.kCompleteArbor == self.Arbor():
      soma = self.RootNode()
      total_area += 4.0 * math.pi * soma.Radius() * soma.Radius()
    return total_area

  def Volume(self):
    total_volume = 0
    for each_section in self.Sections():
      total_volume += each_section.Volume()
    if self.kCompleteArbor == self.Arbor():
      soma = self.RootNode()
      total_volume += (4.0 / 3.0) * math.pi * soma.Radius() * soma.Radius() * soma.Radius()
    return total_volume

  def SpineVolumeAndArea(self):
    """Returns a tuple (total_spine_volume, total_spine_area)."""

    SurfaceAreaOneApicalSpine = (self.kApicalNeckDiam * math.pi * self.kApicalNeckLen +
                                 self.kApicalHeadDiam * math.pi * self.kApicalHeadLen)
    SurfaceAreaOneBasalSpine = (self.kBasalNeckDiam * math.pi * self.kBasalNeckLen +
                                self.kBasalHeadDiam * math.pi * self.kBasalHeadLen)
    VolumeOneApicalSpine = (
        math.pi * (self.kApicalNeckDiam/2.0) * (self.kApicalNeckDiam/2.0) * self.kApicalNeckLen +
        math.pi * (self.kApicalHeadDiam/2.0) * (self.kApicalHeadDiam/2.0) * self.kApicalHeadLen )
    VolumeOneBasalSpine = (
        math.pi * (self.kBasalNeckDiam/2.0) * (self.kBasalNeckDiam/2.0) * self.kBasalNeckLen +
        math.pi * (self.kBasalHeadDiam/2.0) * (self.kBasalHeadDiam/2.0) * self.kBasalHeadLen )

    spine_volume = 0
    spine_area = 0
    if self.kApicalArbor == self.Arbor():
      spine_volume = self.SpineCount() * VolumeOneApicalSpine;
      spine_area = self.SpineCount() * SurfaceAreaOneApicalSpine;
    if self.kBasalArbor == self.Arbor():
      spine_volume = self.SpineCount() * VolumeOneBasalSpine;
      spine_area = self.SpineCount() * SurfaceAreaOneBasalSpine;
    return (spine_volume, spine_area)

  def SpineDensity(self):
    return self.SpineCount() / self.CumulativeLength()

  def SpineAtIndex(self, index):
    if not self._spines:
      return None
    else:
      return self._spines.SpineAtIndex(index)

  def Spines(self):
    return self._spines

  def ConvertToHocFile(self, distinguish_apical_basal, maxApicalRootRadius):
    """Root path should not end in a slash."""
    path = self.HocFilePath(distinguish_apical_basal)

    if self._arbor == self.kApicalArbor or self._arbor == self.kCompleteArbor:
      hocFile = HocFile(path, self, self.MicronsPerPixelZ(),
                        distinguish_apical_basal, maxApicalRootRadius)
    else:
      hocFile = HocFile(path, self, self.MicronsPerPixelZ(),
                        distinguish_apical_basal, "n/a")

    print 'Writing file %s' % path
    hocFile.Write()

  def SpinesMatchNodes(self):
    if not self._swc or not self._spines:
      return false
    swc_path = self.SwcPath()
    spine_path = self.SpinesPath()
    swc = Swc(swc_path)
    spinefile = SpineFile(spine_path)
    swc.Load()
    spinefile.Load(swc)
    spines = spinefile.Spines()
    print "Number of spines: %d" % len(spines)
    good_count = 0
    bad_count = 0
    total_bad_distance_squared = 0
    for each_spine in spines:
      node_id = each_spine.SwcNodeId()
      # Ignore spines attached to the soma
      if -1 == node_id:
        good_count += 1
        continue
      node_offset = each_spine.SwcNodeOffset()
      try:
        node = swc.NodeWithId(node_id)
      except:
        print "Spine references nonexistent node: %d" % node_id
        bad_count += 1
        continue
      # Ignore spines attached to nodes that parent directly on the soma (since
      # it's hard to compute their position, and they're typically part of the
      # soma, too, in terms of the morphology.)
      if (-1 == node.ParentId()):
        continue
      try:
        parent_node = swc.NodeWithId(node.ParentId())
      except:
        print "Could not access parent node: %d" % node.ParentId()
        bad_count += 1
        continue
      putative_attachment_x = node.X() + node_offset * (parent_node.X() - node.X())
      putative_attachment_y = node.Y() + node_offset * (parent_node.Y() - node.Y())
      putative_attachment_z = node.Z() + node_offset * (parent_node.Z() - node.Z())
      attachment_x = each_spine.AttachX()
      attachment_y = each_spine.AttachY()
      attachment_z = each_spine.AttachZ()
      distance_squared = ((putative_attachment_x - attachment_x) *
                            (putative_attachment_x - attachment_x) +
                          (putative_attachment_y - attachment_y) *
                            (putative_attachment_y - attachment_y) +
                          (putative_attachment_z - attachment_z) *
                            (putative_attachment_z - attachment_z))
      if distance_squared > 25:
        bad_count += 1
        total_bad_distance_squared += distance_squared
      else:
        good_count += 1
    print "%d/%d spines validate" % (good_count, len(spines))
    print "Average distance to bad spine: %f" % math.sqrt(total_bad_distance_squared)
    return not (bad_count > (len(spines) * 0.01))

  # The "Standard" soma radius is useful for operations in which a portion of
  # one neuron is compared with a portion of another, and it's desirable to
  # factor the soma out of the comparison by standardizing it between the
  # neurons.
  def SetStandardSomaRadius(self, radius):
    self._standard_soma_radius = radius

  def StandardSomaRadius(self):
    return self._standard_soma_radius

  # For the specified radius, returns a tuple of (radius, number of dendrite
  # intersections, total intersection area, mean branch diameter)
  def Sholl3dForRadius(self, radius):
    intersection_count = 0
    total_area = 0
    total_diameter = 0
    for each_section in self._sections:
      base_distance = self.LengthToSection(each_section)
      if each_section.IntersectsRadius(radius, base_distance):
        diameter = each_section.DiameterOfIntersectionAtDistance(
            radius - base_distance)
        area = math.pi * (diameter / 2.0) * (diameter / 2.0)
        intersection_count += 1
        total_area += area
        total_diameter += diameter
    if intersection_count:
      mean_diameter = total_diameter / intersection_count
      return (radius, intersection_count, total_area, mean_diameter)
    else:
      return (radius, 0, 0, 0)

  def MaximumDistanceAlongDendrite(self):
    max = 0
    for each_section in self._sections:
      tip_distance = self.LengthToSection(each_section) + each_section.Length()
      if tip_distance > max:
        max = tip_distance
    return max

  # Returns a list of tuples, each corresponding to a radius from the soma,
  # each an increasing distance of 'radius_increment' from the last.  Each tuple
  # contains the values: (radius, number of dendrite intersections, total
  # intersection area, mean branch diameter).
  def Sholl3d(self, radius_increment):
    result = []
    for radius in range(radius_increment,
                        int(math.ceil(self.MaximumDistanceAlongDendrite())),
                        radius_increment):
      result.append(self.Sholl3dForRadius(radius))
    return result

  def SpineCountByRadius(self, radius_increment, radius_plus_minus):
    spine_count_by_radius = {}
    for radius in range(0,
                        int(math.ceil(self.MaximumDistanceAlongDendrite()) +
                            radius_increment),
                        radius_increment):
      spine_count_by_radius[radius] = 0
    spines = self._spines.Spines()
    for each_spine in spines:
      distance = self._SpineDistance(each_spine)
      distance += radius_plus_minus
      radius_count = int(math.floor(distance / radius_increment))
      relevant_radius = int(radius_count * radius_increment)
      if distance - relevant_radius <= radius_plus_minus * 2:
        spine_count_by_radius[relevant_radius] += 1
    return spine_count_by_radius

  def SectionLengthByRadius(self, radius_increment, radius_plus_minus):
    section_length_by_radius = {}
    # print self.Name()
    # print "Max distance: ", self.MaximumDistanceAlongDendrite()
    for each_radius in range(0,
                             int(math.ceil(
                                self.MaximumDistanceAlongDendrite()) +
                                    radius_increment),
                             radius_increment):
      section_length_by_radius[each_radius] = 0
    section_length_by_radius[0] = 0
    for each_section in self._sections:
      each_section.SetLengthFromSomaToSection(
          self.LengthToSection(each_section))
      start_distance = each_section.LengthToStartFromSoma() + radius_plus_minus
      radius_count = int(math.floor(start_distance / radius_increment))
      relevant_radius = int(radius_count * radius_increment)
      band_start = relevant_radius - radius_plus_minus
      band_end = relevant_radius + radius_plus_minus
      section_length_in_band = each_section.SectionLengthInBand(band_start,
                                                                band_end)
      while section_length_in_band > 0:
        section_length_by_radius[relevant_radius] += section_length_in_band
        relevant_radius += radius_increment
        band_start = relevant_radius - radius_plus_minus
        band_end = relevant_radius + radius_plus_minus
        section_length_in_band = each_section.SectionLengthInBand(band_start,
                                                                  band_end)
    return section_length_by_radius

  # Populates and returns a list of dictionaries containing the keys
  #   name
  #   radius
  #   spineCount
  #   sectionLength
  def SpineSholl3D(self, radius_increment, radius_plus_minus):
    result = []
    # print self.Name()
    # print "Radius_increment: ", radius_increment
    # print "Radius plus_minus: ", radius_plus_minus
    spine_count = 0
    total_length = 0
    spine_count_by_radius = self.SpineCountByRadius(radius_increment,
                                                    radius_plus_minus)
    section_length_by_radius = self.SectionLengthByRadius(radius_increment,
                                                          radius_plus_minus)
    # print "radius\tspineCount\tsectionLength\tspineDensity"
    for radius in range(radius_increment,
                        int(math.ceil(self.MaximumDistanceAlongDendrite())),
                        radius_increment):
      resultsForRadius = {
        "name": self.Name(),
        "radius": radius,
        "spineCount": spine_count_by_radius[radius],
        "sectionLength": section_length_by_radius[radius]
      }
      result.append(resultsForRadius)
      spine_count += spine_count_by_radius[radius]
      total_length += section_length_by_radius[radius]
    # print "Total spines: ", spine_count
    # print "Total length: ", total_length
    return result


  def _SpineDistance(self, spine):
    return spine.SomaDistance()

  def _NodeDistance(self, node1, node2):
    return math.sqrt(math.pow(node1.X() - node2.X(), 2) +
                     math.pow(node1.Y() - node2.Y(), 2) +
                     math.pow(node1.Z() - node2.Z(), 2))

  def _NodeDistanceDecimal(self, node1, node2):
    x1 = decimal.Decimal(str(node1.X()))
    x2 = decimal.Decimal(str(node2.X()))
    y1 = decimal.Decimal(str(node1.Y()))
    y2 = decimal.Decimal(str(node2.Y()))
    z1 = decimal.Decimal(str(node1.Z()))
    z2 = decimal.Decimal(str(node2.Z()))
    return decimal.Decimal.sqrt(decimal.getcontext().power(x1 - x2, 2) +
                                decimal.getcontext().power(y1 - y2, 2) +
                                decimal.getcontext().power(z1 - z2, 2))

  def LengthToSection(self, section):
    """Returns the length from the section start to the neuron's root node.
       Distance is traced along the dendrite.
    """
    total_length = 0
    current_section = section
    while True:
      parent_id = current_section.ParentId()
      if -1 == parent_id:
        section_start_node = current_section.Nodes()[0]
        soma_node = self._swc.RootNode()
        total_length += self._NodeDistance(section_start_node, soma_node)
        break
      current_section = self.SectionWithId(parent_id)
      total_length += current_section.Length()
    return total_length

  def LengthToNode(self, node):
    """Returns the length from the given node to the neuron's root node.
       Distance is traced along the dendrite.
    """
    total_length = 0
    current_node = node
    reached_soma = False
    while True:
      parent_id = current_node.ParentId()
      if -1 == parent_id:
        total_length += self._NodeDistance(current_node,
                                           self._swc.RootNode())
        break
      parent_node = self.NodeWithId(parent_id)
      total_length += self._NodeDistance(current_node, parent_node)
      current_node = parent_node
    return total_length

  def BoundingBox(self):
    return self._swc.BoundingBox()

  def PrintSpineFileWithCorrectedSomaDistance(self):
    """Prints a spine file with corrected SOMA-DISTANCE.
       The printed spine file is equivalent to the one already loaded by the
       SpineFile class, but all the SomaDistance fields are recomputed.  This
       is necessary to work around a bug in NeuronStudio where this field is
       not updated correctly when a neuron model is edited.
    """
    print "              ID  SECTION-NUMBER  SECTION-LENGTH    BRANCH-ORDER               X               Y               Z   HEAD-DIAMETER   NECK-DIAMETER         MAX-DTS            TYPE            AUTO   XYPLANE-ANGLE     SWC-NODE-ID SWC-NODE-OFFSET        ATTACH-X        ATTACH-Y        ATTACH-Z   SOMA-DISTANCE"
    spines = self._spines.Spines()

    print "decimal precision", decimal.getcontext().prec
    for each_spine in spines:
      auto_text = "no"
      if each_spine.IsAuto():
        auto_text = "yes"
      attachment_node = self.NodeWithId(each_spine.SwcNodeId())
      parent_id = attachment_node.ParentId()
      parent_node = self.NodeWithId(parent_id)
      soma_distance = self.LengthToNode(parent_node)
      soma_distance += (
          self._NodeDistance(parent_node, attachment_node) *
          (1.0 - each_spine.SwcNodeOffset()))

      spinefile_tuple = (each_spine.Id(), each_spine.SectionNumber(),
                         each_spine.SectionLength(), each_spine.BranchOrder(),
                         each_spine.X(), each_spine.Y(), each_spine.Z(),
                         each_spine.HeadDiameter(),
                         float(each_spine.NeckDiameter()),
                         each_spine.MaxDTS(), each_spine.Type(), auto_text,
                         each_spine.XYPlaneAngle(), each_spine.SwcNodeId(),
                         each_spine.SwcNodeOffset(), each_spine.AttachX(),
                         each_spine.AttachY(), each_spine.AttachZ(),
                         soma_distance)
      print "%16d\
%16d\
%16.6f\
%16f\
%16.6f\
%16.6f\
%16.6f\
%16.6f\
%16.6f\
%16.6f\
%16s\
%16s\
%16.6f\
%16d\
%16.6f\
%16.6f\
%16.6f\
%16.6f\
%16.6f" % spinefile_tuple



