#!/usr/bin/python

from lib.SubTree import *
import lib.Neuron
import copy

# Note that discarding of too-large apical sections is only done in HocFile and
# its helper classes SubTree, not in Swc, because only the NEURON-based
# computations make use of a "standard soma" across multiple neurons.

class HocFile:

  def __init__(self, path, neuron, microns_per_pixel_z,
               distinguish_apical_basal, maxApicalRootRadius):
    self._path = path
    self._neuron = neuron
    self._microns_per_pixel_z = microns_per_pixel_z
    self._maxApicalRootRadius = maxApicalRootRadius

    self._subtrees = []
    if distinguish_apical_basal:
      apicalSections = self._neuron.ApicalSections()
      if len(apicalSections) > 0:
        baseSection = apicalSections[0]
        apicalSections[0] = self.ClipWideApicalBaseNodesFromSection(baseSection)
      self._subtrees.append(SubTree(neuron, apicalSections, "apical"))
      self._subtrees.append(SubTree(neuron, self._neuron.BasalSections(),
                            "basal"))
    else:
      self._subtrees.append(SubTree(neuron, self._neuron.Sections(),
                            "whole"))

    for each_tree in self._subtrees:
      each_tree.EliminateSingleNodeSegments()
      each_tree.PruneSpinesNotOnSubtree()

  def SomaDiameter(self):
    return self._neuron.RootNode().Radius() * 2.0

  def SomaLength(self):
    return self._neuron.RootNode().Radius() * 2.0

  def SectionNodeData(self, section):
    """Returns list of (x, y, z, diam) for each node in the section."""
    section_node_data = []
    for each_node in section.Nodes():
      section_node_data.append((each_node.X(), each_node.Y(), each_node.Z(),
                               each_node.Radius() * 2.0))
    return section_node_data

  def ClipWideApicalBaseNodesFromSection(self, section):
    if self._maxApicalRootRadius == "n/a":
      return section
    clippedSection = Section(section.Id(), -1)
    allNodes = []
    preservedNodes = []
    skipping = True
    for eachNode in section.Nodes():
      allNodes.append(eachNode)

    maximumRadius = float(self._maxApicalRootRadius)
    for eachNode in allNodes:
      if skipping and eachNode.Radius() > maximumRadius:
        continue
      skipping = False
      preservedNodes.append(eachNode)

    if len(preservedNodes) < 2:
      preservedNodes = []
      preservedNodes.append(allNodes[-2])
      preservedNodes.append(allNodes[-1])

    for eachNode in preservedNodes:
      clippedSection.AddNode(eachNode)
    for eachChild in section.Children():
      clippedSection.AddChild(eachChild)
    clippedSection.ClipStartingNodesLargerThanRadius(
        float(self._maxApicalRootRadius))
    return clippedSection

  def Write(self):
    file = open(self._path, 'w')

    file.write('create soma\n')
    for each_subtree in self._subtrees:
      file.write('create dend_%s[%s]\n' % (each_subtree.Name(),
                                           each_subtree.SectionCount()))
      file.write('create spine_%s[%s]\n' % (each_subtree.Name(),
                                           each_subtree.SpineCount()))
    file.write('\n')
    file.write('access soma\n\n')

    file.write('proc geometry() { local i, j\n')

    file.write('soma {\n')
    file.write('  L = %f\n' % self.SomaLength())
    file.write('  diam = %f\n' % self.SomaDiameter())
    file.write('}\n\n')

    # Connect dendrites to soma
    for each_subtree in self._subtrees:
      section_indices = each_subtree.SectionIndicesConnectedToSoma()
      for each_index in section_indices:
        file.write('connect dend_%s[%d](0), soma(0.5)\n' % (each_subtree.Name(),
                                                            each_index))
    file.write('\n')

    # At this point, it would be convenient to just issue all the commands
    # to build the neuron.  But neuron has a limit on the size of a function
    # that also applies to files that are passed to xopen().  Our neurons are
    # detailed enough that it's trivial for them to go over that limit.
    # Instead, we'll create short function that reads large lists of data later
    # in the file, using a NEURON feature that lets you fscan() on the same
    # file that defines a function.

    # A tricky point is that NEURON's "for a,b" construct includes both
    # a and b, unlike the usual C (for i = a; i < b; ++i), which does not
    # include b, or Python's xrange() function.

    # Define dendrites: hoc
    for each_subtree in self._subtrees:
      file.write("for i = 0, %d {\n" % (len(each_subtree.Sections()) - 1))
      file.write("  dend_%s[i] {\n" % each_subtree.Name())
      file.write("    pt3dclear()\n")
      file.write("    for j = 1, fscan() {\n")
      file.write("      pt3dadd(fscan(), fscan(), fscan(), fscan())\n")
      file.write("    }\n")
      file.write("  }\n")
      file.write("}\n")

    # Define spines: hoc
    for each_subtree in self._subtrees:
      file.write("for i = 0, %d {\n" % (len(each_subtree.SpineGeometryData()) - 1))
      file.write("  spine_%s[i] {\n" % each_subtree.Name())
      file.write("    pt3dclear()\n")
      file.write("    for j = 1, fscan() {\n")
      file.write("      pt3dadd(fscan(), fscan(), fscan(), fscan())\n")
      file.write("    }\n")
      file.write("  }\n")
      file.write("}\n")

    # Connect dendrites: hoc
    for each_subtree in self._subtrees:
      file.write("for i = 0, %d {\n" % (len(each_subtree.DendriteConnectionListByIndex()) - 1))
      file.write("  connect dend_%s[fscan()](0), dend_%s[fscan()](1)\n" % (each_subtree.Name(),
                                                                           each_subtree.Name()))
      file.write("}\n\n")

    # Connect spines: hoc
    for each_subtree in self._subtrees:
      file.write("for i = 0, %d {\n" % (len(each_subtree.SectionIdsWithSpines()) - 1))
      file.write("  for j = 1, fscan() {\n" )
      file.write("    dend_%s[fscan()] {\n" % each_subtree.Name())
      file.write("      connect spine_%s[fscan()](0), fscan()\n" % each_subtree.Name())
      file.write("    }\n")
      file.write("  }\n")
      file.write("}\n\n")

    file.write('}\n\n')  # Ends the geometry() function
    file.write('geometry()\n\n\n\n')

    # Define dendrites: data
    file.write("DENDRITES:\n\n")

    for each_subtree in self._subtrees:
      file.write("dend_%s:\n" % each_subtree.Name())
      for each_section in each_subtree.Sections():
        node_data = self.SectionNodeData(each_section)
        file.write('   %d\n' % len(node_data))
        for each_node in node_data:
          file.write('    %f %f %f %f\n' % each_node)
        file.write('\n\n')

    file.write("SPINES:\n\n")
    for each_subtree in self._subtrees:
      file.write("dend_%s:\n" % each_subtree.Name())
      spine_data = each_subtree.SpineGeometryData()
      for each_spine in spine_data:
        file.write('   2\n')
        file.write('    %f %f %f %f\n' % (each_spine[0], each_spine[1],
                                          each_spine[2], each_spine[3]))
        file.write('    %f %f %f %f\n' % (each_spine[4], each_spine[5],
                                          each_spine[6], each_spine[7]))
        file.write('\n\n')

    # Connect dendrites: data
    file.write('DENDRITE CONNECTIVITY:\n\n')
    for each_subtree in self._subtrees:
      file.write("dend_%s:\n" % each_subtree.Name())
      dendrite_connections = each_subtree.DendriteConnectionListByIndex()
      for each_connection in dendrite_connections:
        file.write('    %d %d\n' % each_connection)
      file.write('\n\n')

    # Connect spines: data
    file.write('SPINE CONNECTIVITY:\n\n')
    for each_subtree in self._subtrees:
      file.write("dend_%s:\n" % each_subtree.Name())
      section_ids = each_subtree.SectionIdsWithSpines()
      for each_section_id in section_ids:
        spine_connections = each_subtree.SpineConnectionListByIndex(each_section_id)
        file.write('   %d\n' % len(spine_connections))
        for each_spine in spine_connections:
          file.write('      %d  %d  %f\n' % each_spine)
        file.write('\n')

    file.close()
