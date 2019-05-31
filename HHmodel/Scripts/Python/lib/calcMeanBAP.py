#! /usr/bin/python

import math

def isNotEmpty(string):
  return ('' != string)

# Returns the interpolated y value at the given x, assuming that x lies
# on a line between (x1, y1) and (x2, y2).
def interpolatedValue(x, x1, y1, x2, y2):
  xdist = x - x1
  ytotal = y2 - y1
  xtotal = x2 - x1
  y = ((xdist/xtotal) * ytotal) + y1
  return y

# Compares the first items of list1 and list2, and returns the greater one,
# as a single-element list (this makes it easy to use in a reduce statement.
# This function might not be needed; it hasn't been tested yet.
def max_first(list1, list2):
  x = list1[0]
  y = list2[0]
  max_val = max(x,y)
  return [max_val]

# Sets up the list of every-one-micron x values, to be populated with the
# "average" BAP value at each point.  This just sets up a data structure with
# the correct number of elements for efficiency purposes; it doesn't populate
# it.
def prepare_x_values(data):
  max_x = reduce(max_first, data)
  max_x_int = int(math.ceil(max_x[0]))
  per_x_values = []
  for x in range(0, max_x_int + 1):
    per_x_values.append([])
  return per_x_values

def add(x, y): return x + y

def scan_data_old(data, output):
  (x_last, y_last) = data[0]
  data = data[1:]
  for (x, y) in data:
    if (x < x_last):
      # Starting a new branch
      if (x == round(x)):
        # the new point is on a micron boundary, so store it.
        output[int(x)].append(y)
        continue
      else:
        # the new point should be used as a new baseline
        (x_last, y_last) = (x, y)
        continue
    else:
      # We're proceeding down a branch
      x_last_int = int(math.floor(x_last))
      x_int = int(math.floor(x))
      # The range will only be iterated if x_last_int and x_int have different
      # floors.
      for x_val in range(x_last_int, x_int):
        output[x_val].append(interpolatedValue(x_val, x_last, y_last, x, y))
    (x_last, y_last) = (x, y)
  return output

# Strips an unbranched section off the front of the data array and returns it,
# removing it from the tree in the process.  The remainder of data is suitable
# for processing.
def extract_section(data):
  # Begin by stripping off an unbranched section
  count = 0
  x_last = -1
  section = []
  for (x, y) in data:
    if (x < x_last):
      # strip the branch off the data
      del data[0:count]
      break
    else:
      section.append([x, y])
      x_last = x
      count += 1
  if count == len(data):  # This happens when we reach the end of the data set
    del data[0:count]
  return section

# Checks if two floats are equal to within 0.00001
def float_equals(lhs, rhs):
  return (math.fabs(lhs - rhs) < 0.00001)

# Rounds the positive floating point number fnum to the nearest integer value
# (returned as a float).
def round(fnum):
  if (fnum - math.floor(fnum)) < 0.5:
    return math.floor(fnum)
  else:
    return math.ceil(fnum)

# Computes the y values of an unbranched section at integer points 0..1..x
# to the maximum x value in the section, interpolating where necessary
def apply_section_to_x_values(section, per_x_values):
#  print "===== new section ====="

  # target_x is the x value we want to store; it steps by 1 micron increments
  first_x_in_section = section[0][0]

  # set target_x to the first int x value in the section; bear in mind that if
  # the first x value is, say, 12.0000000003, we want to treat it as 12.  Otherwise,
  # round up to the next integer x value that's inside the section.
  if float_equals(first_x_in_section, round(first_x_in_section)):
#    print "first x: %s, rounded: %s, int-rounded: %s" % (first_x_in_section,
#                                                         round(first_x_in_section),
#                                                         int(round(first_x_in_section)))
    target_x = int(round(first_x_in_section))
  else:
    target_x = int(math.ceil(first_x_in_section))

#  print "Target x: %s" % target_x
  x_last = -1
  y_last = -1
  section_index = 0
  for (x, y) in section:
#    print "%s...    (x_last = %s)" % (x, x_last)
    if float_equals(x, target_x):
#      print "equal... appending %s" % y
      per_x_values[target_x].append(y)
      target_x += 1
#      print "Target x: %s" % target_x
    else:
      # Scan forward to the x in the next section, filling in interpolated
      # points as you go.  Note that per_x_values is intended to be re-used
      # between calls to this function, so that it will include one entry
      # for each branch.  Any given call of this function, however, will only
      # add a single value for each value of x.
      while (x_last < target_x) and (target_x <= x):
        y_val = interpolatedValue(target_x, x_last, y_last, x, y)
#        print "%s < %s < %s ... appending %s" % (x_last, target_x, x, y_val)
        per_x_values[target_x].append(y_val)
        target_x += 1
#        print "Target x: %s" % target_x
    x_last = x
    y_last = y


def average(input_list):
  if len(input_list):
    sum = reduce(add, input_list)
    return sum / len(input_list)
  else:
    return 0

def compute_average(output):
  output = [average(each_list) for each_list in output]
  return output

# Converts average value into an x, y table
def tablefy(input_list):
  result = []
  for i in range(0, len(input_list)):
    result.append([i, input_list[i]])
  return result

# Compute the area under the average line.  The interval between the average
# values is always 1, which simplifies things.  Compute the area with a
# trapezoidal approximation.
def calc_area(average_values):
  sum = 0.0
  for i in range(0, len(average_values) - 1):
    ave_value = (average_values[i] + average_values[i+1]) / 2.0
    sum += ave_value
  return sum

# Given an array of values, indexed by x position, where each element is an
# array of voltage values, print the table.
def print_values_by_x(per_x_values):
  for i in range(0, len(per_x_values)):
    for j in range(0, len(per_x_values[i])):
      print "%s, %s" % (i, per_x_values[i][j])

def print_averages_by_x(per_x_values):
  for i in range(0, len(per_x_values)):
    if len(per_x_values[i]) > 0:
      print "%f\t%f\t%f " % (i, sum(per_x_values[i]) / len(per_x_values[i]), len(per_x_values[i]))

def print_list(data):
  for i in range(0, len(data)):
    print "%s\t%s" % (data[i][0], data[i][1])
  print "============================="

def discretize_to_one_micron_bins(data):
  """Converts raw mbap data to a format better suited to computation.

     The data that comes back from NEURON has x values that have been
     determined by the NSEG during the simulation.  These can't be used
     directly for averaging the voltage (y) values, since it's not clear
     which points should be added.  So, this function takes the x values
     and bins them into 1-micron intervals, so that they can be summed
     on a per-x basis.
  """
  per_x_values = prepare_x_values(data)
  while len(data):
    section = extract_section(data)
    apply_section_to_x_values(section, per_x_values)
  return per_x_values


def ComputeNBPArea(data):
  """Computes mean NBPArea given data of response to an action potential.

     data -> a list of tuples (arclength from soma, maximum displacement from rest potential.  The
     data is assumed to be ordered based on a depth-first traversal of the tree, starting at the
     soma, such that any time forward traversal of the list results in a decrease in the arclength
     value, it indicates the terminus of a branch."""
  per_x_values = discretize_to_one_micron_bins(data)
  per_x_values = compute_average(per_x_values)
  area = calc_area(per_x_values)
  # We can treat the arclength as just the length of per_x_values because we've
  # discretized at a resolution of 1 micron.
  nbp_area = area/(len(per_x_values) - 1)
  return nbp_area

