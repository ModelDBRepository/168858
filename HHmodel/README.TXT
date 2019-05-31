This directory was written by Patrick J Coskren, pcoskren@icloud.com .  
Last modified August 2014.

This is the project directory for the second paper with the Hof
lab.  A particular goal is being able to easily regenerate the papers 
computations in a turnkey fashion.

To run, execute the file Scripts/regeneratePaperComputations.sh from the same
directory containing this README.TXT file, like so:

bash ./Scripts/regeneratePaperComputations.sh

While this is a little awkward to invoke, it avoids a lot of "../" paths inside
the script, which I considered to be the larger gain.

Scripts/ParameterSets.csv contains a list of named parameter sets which are
selected in the first non-comment line of regeneratePaperComputations.sh.  You
can modify it there to choose to run all the simulations with a different set
of parameters.  All the .hoc scripts have been modified to get their parameters
from here.

The regeneratePaperComputations.sh assumes your computer has a copy of GNU
parallel, an extremely handy utility that takes a set of commands and splits
them across multiple CPU cores, collating the results for you.
<http://www.gnu.org/software/parallel/>  For computations like the ones here,
that are largely independent of each other and require little RAM or disk space,
this gives a nearly linear speedup with the number of cores.  On some systems,
you may want to add an extra argument to the calls to parallel that sets the
number of cores manually: this is because some Intel chips provide
"hyperthreading", which looks to the operating system like two CPU cores for
every single CPU core that's present.  This is handy when you're running lots of
jobs that aren't CPU-bound (which is the typical case in most computers), but
when the CPU is the limiting factor, hyperthreading just adds overhead, and
you're better off manually setting the number of cores to what you really have.
See 'man parallel' for details.  The extra overhead isn't that much, so if
you're not sure whether your CPU uses hyperthreading, there's no harm in just
not worrying about it.

Another goal of this code re-organization was to move all computation (stats,
generally) from Excel to R; not because I have a problem with spreadsheets per
se, but because I found they made it difficult to audit the formulas to be
certain they were doing what I thought they were.  Moving all the data tables to
.CSV and all the computations to R provides an extra degree of transparency and
reproducibility.

The code in Scripts/NeuronMechanims will need to be rebuilt with nrnivmodl on
the host system.

The only purpose of NumericalResults-Baseline was to provide something to diff
against when I modified the scripts in a way that was intended just to clean up
code, just to make sure that I didn't break something in the process.
