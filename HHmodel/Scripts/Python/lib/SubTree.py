#!/usr/bin/python

from lib.Neuron import *
from lib.Section import *
from lib.SpineFile import *

import copy

class SubTree:
  """Maintain a group of unbranched segments, with connectivity information."""

  def __init__(self, neuron, section_list, name):
    self._section_list = copy.copy(section_list)
    for each_section in self._section_list:
      # The children in each section will be references to the original section
      # list, not the copy in this class.  So make sure we don't use them by
      # accident.
      each_section.ClearChildren()
    self._name = name
    self._spines = neuron.Spines().Spines()

    self._neuron = neuron

    # Cache of sections by id.
    self._sections_by_id = {}
    self._section_indices_by_id = {}
    self._spines_by_section_id = {}
    self._spine_indices_by_id = {}

    self.RegenerateCaches()

  def Name(self):
    return self._name

  def RegenerateCaches(self):
    self.RegenerateSectionsById()
    self.RegenerateSectionIndicesById()
    self.RegenerateSpinesBySectionId()
    self.RegenerateSpineIndicesById()

  def RegenerateSectionsById(self):
    self._sections_by_id = {}
    for each_section in self._section_list:
      self._sections_by_id[each_section.Id()] = each_section

  def RegenerateSectionIndicesById(self):
    self._section_indices_by_id = {}
    index = 0
    for each_section in self._section_list:
      self._section_indices_by_id[each_section.Id()] = index
      index += 1

  def RegenerateSpinesBySectionId(self):
    self._spines_by_section_id = {}
    for each_spine in self._spines:
      node_id = each_spine.SwcNodeId()
      node = self._neuron.NodeWithId(node_id)
      if not node:
        print ("Error generating subtree %s: spine (id: %d) refers to "
            "nonexistent node (id: %d)") % (self._name, each_spine.Id(),
                                            node_id)
        return
      section = self._neuron.SectionForNode(node)
      if not section.Id() in self._spines_by_section_id:
        self._spines_by_section_id[section.Id()] = []
      self._spines_by_section_id[section.Id()].append(each_spine)

  def RegenerateSpineIndicesById(self):
    self._spine_indices_by_id = {}
    index = 0
    for each_spine in self._spines:
      self._spine_indices_by_id[each_spine.Id()] = index
      index += 1

  def SectionForSectionId(self, section_id):
    return self._sections_by_id[section_id]

  def ReparentSectionChildren(self, section):
    overall_parent = section.ParentId()
    for each_section_id in section.ChildrenSectionIds():
      each_section = self.SectionForSectionId(each_section_id)
      each_section.SetParentId(overall_parent)

  def EliminateSingleNodeSegments(self):
    """Invalidates all section indices."""
    sections_to_remove = []  # List of indices into self._section_list
    index = 0
    for each_section in self._section_list:
      if len(each_section.Nodes()) == 1:
        self.ReparentSectionChildren(each_section)
        sections_to_remove.append(index)
      index += 1
    sections_to_remove.reverse()
    for each_index in sections_to_remove:
      self._section_list.pop(each_index)
    self.RegenerateCaches()

  def PruneSpinesNotOnSubtree(self):
    spines = []
    for each_spine in self._spines:
      node_id = each_spine.SwcNodeId()
      node = self._neuron.NodeWithId(node_id)
      if not node:
        continue
      section = self._neuron.SectionForNode(node)
      if section.Id() in self._sections_by_id:
        spines.append(each_spine)
    self._spines = spines
    self.RegenerateCaches()

  def SectionCount(self):
    return len(self._section_list)

  def SpineCount(self):
    return len(self._spines)

  def Sections(self):
    return self._section_list

  def SectionIndicesConnectedToSoma(self):
    """Returns the indices of all soma-connected sections.

    Returned indices are positions in the list of sections maintained by this list
    and returned by Sections().
    """
    indices = []
    index = 0
    for each_section in self._section_list:
      if each_section.ParentId() == -1:
        indices.append(index)
      index += 1
    return indices

  def SpineGeometryData(self):
    """Returns a list of tuples, one per spine, describing its geometry.
       Each tuple consists of: (attach_x, attach_y, attach_z, neck diameter,
       spine_x, spine_y, spine_z, head diameter).

       Note: this builds a very simple spine, akin to what Doron had, except
       that I'm going to use a diameter of 0.5 instead of 1.0, because that
       seems closer to the values I'm seeing in the spine files.  In a later
       iteration, we can build a more detailed spine using the head diameter,
       neck diameter, and type from the spine file, but it's not clear that
       the image data really has enough resolution to support this anyway.
    """
    spine_geometry_data = []
    for each_spine in self._spines:
      spine_geometry_data.append((each_spine.AttachX(), each_spine.AttachY(),
                                  each_spine.AttachZ(), 0.5, each_spine.X(),
                                  each_spine.Y(), each_spine.Z(), 0.5))
    return spine_geometry_data

  def DendriteConnectionListByIndex(self):
    """Returns a list of tuples (child index, parent index), where both values
       are indices into the section list returned by this object's Sections()
       method."""
    dendrite_connection_list = []
    for each_section in self._section_list:
      if each_section.ParentId() != -1:
        each_section_index = self._section_indices_by_id[each_section.Id()]
        each_section_parent_index = self._section_indices_by_id[
            each_section.ParentId()]
        dendrite_connection_list.append((each_section_index, each_section_parent_index))
    return dendrite_connection_list

  def SectionIdsWithSpines(self):
    section_ids = []
    for each_section in self._section_list:
      if each_section.Id() in self._spines_by_section_id and \
          len(self._spines_by_section_id[each_section.Id()]) > 0:
        section_ids.append(each_section.Id())
    return section_ids

  def SpineConnectionListByIndex(self, section_id):
    """Returns a list of tuples (index of section in this object's Sections()
       list, index of spine in this object's list of spines, fraction of the
       length of the section along which the spine is located."""
    spine_connection_list = []
    section = self._sections_by_id[section_id]
    section_index = self._section_indices_by_id[section.Id()]
    for each_spine in self._spines_by_section_id[section.Id()]:
      spine_index = self._spine_indices_by_id[each_spine.Id()]
      node = self._neuron.NodeWithId(each_spine.SwcNodeId())
      fraction = section.PercentageLengthOfNode(node)
      spine_connection_list.append((section_index, spine_index, fraction))
    return spine_connection_list
