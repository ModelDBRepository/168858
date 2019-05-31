#!/usr/bin/python

import sys

class ParameterSet:
  def __init__(self):
    self._name = "unnamed"
    self._ePas = "-70"
    self._V0 = "-70"
    self._stdSomaRadius = "0"
    self._membraneCapacitance = "1"
    self._membraneResistance = "150"
    self._axialResistivity = "20000"
    self._celsius = "21"
    self._gNa = "100"
    self._gKv = "100"
    self._geomNsegDlambda = "0.1"
    self._geomNsegDlambdaForFiringRates = "0.1"
    self._maxApicalRootRadius = "-1"  # i.e. don't trip apical root nodes.
    self._comments = ""

  def populateFromCsvRow(self, csvRow):
    csvRow = csvRow.strip()
    csvItems = csvRow.split(",")
    if len(csvItems) != 14:
      print "Error: Parameter set row has an incorrect number of elements: ", len(csvItems)
      sys.exit(1)
    (self._name, self._ePas, self._V0, self._stdSomaRadius,
     self._membraneCapacitance, self._membraneResistance,
     self._axialResistivity, self._celsius, self._gNa, self._gKv,
     self._geomNsegDlambda, self._geomNsegDlambdaForFiringRates,
     self._maxApicalRootRadius, self._comments) = csvItems

  def name(self):
    return self._name

  def ePas(self):
    return self._ePas

  def V0(self):
    return self._V0

  def stdSomaRadius(self):
    return self._stdSomaRadius

  def membraneCapacitance(self):
    return self._membraneCapacitance

  def membraneResistance(self):
    return self._membraneResistance

  def axialResistivity(self):
    return self._axialResistivity

  def celsius(self):
    return self._celsius

  def gNa(self):
    return self._gNa

  def gKv(self):
    return self._gKv

  def geomNsegDlambda(self):
    return self._geomNsegDlambda

  def setGeomNsegDlambda(self, geomNsegDlambda):
    self._geomNsegDlambda = geomNsegDlambda

  def geomNsegDlambdaForFiringRates(self):
    return self._geomNsegDlambdaForFiringRates

  def maxApicalRootRadius(self):
    return self._maxApicalRootRadius

  def comments(self):
    return self._comments

  def setGNa(self, gNa):
    self._gNa = gNa

  def setKv(self, gKv):
    self._gKv = gKv

  def dict(self):
    """Returns a copy of the ParameterSet's data."""
    result = {}
    result["name"] = self.name()
    result["ePas"] = self.ePas()
    result["V0"] = self.V0()
    result["stdSomaRadius"] = self.stdSomaRadius()
    result["membraneCapacitance"] = self.membraneCapacitance()
    result["membraneResistance"] = self.membraneResistance()
    result["axialResistivity"] = self.axialResistivity()
    result["celsius"] = self.celsius()
    result["gNa"] = self.gNa()
    result["gKv"] = self.gKv()
    result["geomNsegDlambda"] = self.geomNsegDlambda()
    result["geomNsegDlambdaForFiringRates"] = self.geomNsegDlambdaForFiringRates()
    result["maxApicalRootRadius"] = self.maxApicalRootRadius()
    return result

  def __str__(self):
    return """\
ParameterSet
  name: %s
  ePas: %s
  V0: %s
  stdSomaRadius: %s
  membraneCapacitance: %s
  membraneResistance: %s
  axialResistivity: %s
  celsius: %s
  gNa: %s
  gKv: %s
  geomNsegDlambda: %s
  geomNsegDlambdaForFiringRates: %s
  maxApicalRootRadius: %s
  comments: %s""" % (self.name(), self.ePas(), self.V0(), self.stdSomaRadius(),
                     self.membraneCapacitance(), self.membraneResistance(),
                     self.axialResistivity(), self.celsius(), self.gNa(),
                     self.gKv(), self.geomNsegDlambda(),
                     self.geomNsegDlambdaForFiringRates(),
                     self.maxApicalRootRadius(), self.comments())
